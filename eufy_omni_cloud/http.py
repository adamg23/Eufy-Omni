"""HTTPS side of the Eufy Clean cloud: login, account info, device list, MQTT credentials."""

from __future__ import annotations

import hashlib
import logging
import secrets
from dataclasses import dataclass, field
from typing import Any

import aiohttp

from .const import (
    AIOT_DEVICE_LIST,
    AIOT_MQTT_INFO,
    CLOUD_DEVICE_LIST,
    LOGIN_CLIENTS,
    USER_AGENT,
    USER_CENTER_INFO,
)
from .exceptions import EufyAuthError, EufyConnectionError, EufyRateLimited

_LOGGER = logging.getLogger(__name__)
_TIMEOUT = aiohttp.ClientTimeout(total=30)
_SECRET_HINTS = ("token", "secret", "key", "email", "pem")


def new_openudid() -> str:
    """A per-installation pseudo device id, like the app generates on first run."""
    return secrets.token_hex(16)


@dataclass
class Session:
    access_token: str
    user_id: str
    login_client: str
    user_center_id: str | None = None
    user_center_token: str | None = None
    raw_login: dict[str, Any] = field(default_factory=dict, repr=False)
    raw_user: dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def gtoken(self) -> str | None:
        if not self.user_center_id:
            return None
        return hashlib.md5(self.user_center_id.encode()).hexdigest()  # noqa: S324 - protocol requirement

    def __repr__(self) -> str:
        return f"Session(login_client={self.login_client!r}, has_user_center={bool(self.user_center_token)})"


@dataclass
class MqttCredentials:
    endpoint: str
    thing_name: str = field(repr=False)
    app_name: str = "eufy_home"
    user_id: str = field(default="", repr=False)
    certificate_pem: str = field(default="", repr=False)
    private_key: str = field(default="", repr=False)
    ca_pem: str | None = field(default=None, repr=False)
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> MqttCredentials:
        try:
            return cls(
                endpoint=data["endpoint_addr"],
                thing_name=data["thing_name"],
                app_name=data["app_name"],
                user_id=data["user_id"],
                certificate_pem=data["certificate_pem"],
                private_key=data["private_key"],
                ca_pem=data.get("aws_root_ca1_pem"),
                raw=data,
            )
        except KeyError as err:
            raise EufyConnectionError(f"MQTT credential response missing {err}") from err


class EufyCloudHttp:
    def __init__(self, username: str, password: str, openudid: str, session: aiohttp.ClientSession) -> None:
        self._username = username
        self._password = password
        self._openudid = openudid
        self._http = session
        self.session: Session | None = None

    @property
    def openudid(self) -> str:
        return self._openudid

    # ----------------------------------------------------------------- login

    async def async_login(self) -> Session:
        """Log in, preferring the client that gives a user-center token."""
        fallback: Session | None = None
        rate_limited = False
        for label, url, client_id, client_secret, category in LOGIN_CLIENTS:
            try:
                sess = await self._try_login(label, url, client_id, client_secret, category)
            except EufyRateLimited:
                rate_limited = True
                continue
            if sess is None:
                continue
            await self._fill_user_center(sess)
            if sess.user_center_token:
                self.session = sess
                return sess
            fallback = fallback or sess
        if fallback is None:
            if rate_limited:
                raise EufyRateLimited("Eufy login rate limit (HTTP 429); wait a few minutes")
            raise EufyAuthError("Login rejected by both Eufy login endpoints")
        self.session = fallback
        return fallback

    async def _try_login(
        self, label: str, url: str, client_id: str, client_secret: str, category: str
    ) -> Session | None:
        headers = {
            "category": category,
            "Accept": "*/*",
            "openudid": self._openudid,
            "Content-Type": "application/json",
            "clientType": "1",
            "User-Agent": USER_AGENT,
        }
        body = {
            "email": self._username,
            "password": self._password,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        try:
            async with self._http.post(url, json=body, headers=headers, timeout=_TIMEOUT) as resp:
                data = await _json_or_none(resp)
                if resp.status == 200 and data and data.get("access_token"):
                    return Session(
                        access_token=data["access_token"],
                        user_id=str(data.get("user_id", "")),
                        login_client=label,
                        raw_login=data,
                    )
                _LOGGER.debug("login %s refused: %s %s", label, resp.status, _safe(data))
                if resp.status == 429:
                    raise EufyRateLimited(f"login {label}: HTTP 429")
                return None
        except aiohttp.ClientError as err:
            raise EufyConnectionError(f"login {label}: {type(err).__name__}") from err

    async def _fill_user_center(self, sess: Session) -> None:
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": USER_AGENT,
            "category": "Home",
            "token": sess.access_token,
            "openudid": self._openudid,
            "clienttype": "2",
        }
        try:
            async with self._http.get(USER_CENTER_INFO, headers=headers, timeout=_TIMEOUT) as resp:
                data = await _json_or_none(resp)
        except aiohttp.ClientError as err:
            raise EufyConnectionError(f"user_center_info: {type(err).__name__}") from err
        if resp.status == 200 and data and data.get("user_center_id"):
            sess.user_center_id = data["user_center_id"]
            sess.user_center_token = data.get("user_center_token")
            sess.raw_user = data
        else:
            _LOGGER.debug("user_center_info gave no user_center_id: %s %s", resp.status, _safe(data))

    # ------------------------------------------------------------- requests

    def _aiot_headers(self) -> dict[str, str]:
        sess = self._require_user_center()
        return {
            "user-agent": USER_AGENT,
            "openudid": self._openudid,
            "os-version": "Android",
            "model-type": "PHONE",
            "app-name": "eufy_home",
            "x-auth-token": sess.user_center_token or "",
            "gtoken": sess.gtoken or "",
            "content-type": "application/json; charset=UTF-8",
        }

    def _require_user_center(self) -> Session:
        if self.session is None:
            raise EufyAuthError("Not logged in")
        if not self.session.user_center_token:
            raise EufyAuthError("Account has no user-center token; AIoT devices unavailable")
        return self.session

    async def async_aiot_devices(self) -> list[dict[str, Any]]:
        """Devices known to the AIoT (MQTT) side, each with its latest `dps` snapshot."""
        try:
            async with self._http.post(
                AIOT_DEVICE_LIST, json={"attribute": 3}, headers=self._aiot_headers(), timeout=_TIMEOUT
            ) as resp:
                data = await _json_or_none(resp)
        except aiohttp.ClientError as err:
            raise EufyConnectionError(f"get_device_list: {type(err).__name__}") from err
        if resp.status in (401, 403):
            raise EufyAuthError(f"get_device_list: HTTP {resp.status}")
        if resp.status != 200 or not isinstance(data, dict):
            raise EufyConnectionError(f"get_device_list: HTTP {resp.status}")
        records = (data.get("data") or {}).get("devices") or []
        return [r["device"] for r in records if isinstance(r, dict) and "device" in r]

    async def async_cloud_devices(self) -> list[dict[str, Any]]:
        """Legacy device list; carries product code and friendly names."""
        if self.session is None:
            raise EufyAuthError("Not logged in")
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": USER_AGENT,
            "category": "Home",
            "token": self.session.access_token,
            "openudid": self._openudid,
            "clienttype": "2",
        }
        try:
            async with self._http.get(CLOUD_DEVICE_LIST, headers=headers, timeout=_TIMEOUT) as resp:
                data = await _json_or_none(resp)
        except aiohttp.ClientError as err:
            raise EufyConnectionError(f"device/v2: {type(err).__name__}") from err
        if resp.status != 200 or not isinstance(data, dict):
            _LOGGER.debug("device/v2 failed: %s", resp.status)
            return []
        return data.get("devices") or []

    async def async_mqtt_credentials(self) -> MqttCredentials:
        try:
            async with self._http.post(
                AIOT_MQTT_INFO, json={}, headers=self._aiot_headers(), timeout=_TIMEOUT
            ) as resp:
                data = await _json_or_none(resp)
        except aiohttp.ClientError as err:
            raise EufyConnectionError(f"get_user_mqtt_info: {type(err).__name__}") from err
        if resp.status in (401, 403):
            raise EufyAuthError(f"get_user_mqtt_info: HTTP {resp.status}")
        if resp.status != 200 or not isinstance(data, dict) or not isinstance(data.get("data"), dict):
            raise EufyConnectionError(f"get_user_mqtt_info: HTTP {resp.status}")
        return MqttCredentials.from_response(data["data"])


async def _json_or_none(resp: aiohttp.ClientResponse) -> Any:
    try:
        return await resp.json(content_type=None)
    except (aiohttp.ContentTypeError, ValueError):
        return None


def _safe(data: Any) -> Any:
    """Strip anything token-shaped before it reaches a log line."""
    if not isinstance(data, dict):
        return data
    return {
        k: ("<redacted>" if any(s in k.lower() for s in _SECRET_HINTS) else v)
        for k, v in data.items()
    }
