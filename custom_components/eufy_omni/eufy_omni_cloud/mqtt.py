"""MQTT transport to Eufy's AWS IoT broker, authenticated with the per-account client certificate.

Message envelope (both directions), JSON over MQTT:

    {"head": {...}, "payload": "<JSON string>"}
    payload = {"account_id": ..., "device_sn": ..., "protocol": 2, "t": <ms>, "data": {"<dp>": value, ...}}

`data` is a Tuya-style data point dict; protobuf values are base64 strings (see codec.py).
Status arrives on cmd/eufy_home/{model}/{sn}/res, the live map stream on biz/.../res.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import secrets
import ssl
import tempfile
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import paho.mqtt.client as mqtt

from .const import MQTT_KEEPALIVE_S, MQTT_PORT, TOPIC_BIZ_RES, TOPIC_CMD_REQ, TOPIC_CMD_RES
from .exceptions import EufyConnectionError
from .http import MqttCredentials

_LOGGER = logging.getLogger(__name__)

DpsCallback = Callable[[str, dict[str, Any]], Awaitable[None] | None]
RawCallback = Callable[[str, bytes], Awaitable[None] | None]


def _build_ssl_context(creds: MqttCredentials) -> ssl.SSLContext:
    """Client-certificate TLS context. Python's ssl only loads key pairs from files, so the
    PEMs are written to a private temp dir, loaded, and deleted again straight away."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_default_certs()
    if creds.ca_pem:
        ctx.load_verify_locations(cadata=creds.ca_pem)
    tmpdir = Path(tempfile.mkdtemp(prefix="eufy-omni-"))
    try:
        cert = tmpdir / "client.crt"
        key = tmpdir / "client.key"
        cert.write_text(creds.certificate_pem, encoding="ascii")
        key.write_text(creds.private_key, encoding="ascii")
        try:
            os.chmod(key, 0o600)
        except OSError:
            pass
        ctx.load_cert_chain(certfile=str(cert), keyfile=str(key))
    finally:
        for p in tmpdir.iterdir():
            try:
                p.unlink()
            except OSError:
                pass
        try:
            tmpdir.rmdir()
        except OSError:
            pass
    return ctx


class EufyMqtt:
    """One broker connection shared by all devices on the account."""

    def __init__(self, creds: MqttCredentials, openudid: str, *, tap_requests: bool = False) -> None:
        self._creds = creds
        self._openudid = openudid
        # Diagnostics only: also subscribe to the request topics to see what other clients
        # (the phone app) send the robot. Never enabled by the integration.
        self.tap_requests = tap_requests
        self._client_id = f"android-{creds.app_name}-eufy_android_{openudid}_{creds.user_id}-{int(time.time() * 1000)}"
        self._loop: asyncio.AbstractEventLoop | None = None
        self._client: mqtt.Client | None = None
        self._connected = asyncio.Event()
        self._closed = False
        # (model, sn) -> callbacks
        self._devices: dict[tuple[str, str], tuple[DpsCallback | None, RawCallback | None]] = {}
        self._seq = 0
        self.last_subscribe_codes: list[int] = []
        self.on_connection_change: Callable[[bool], None] | None = None

    @property
    def connected(self) -> bool:
        return self._connected.is_set()

    @property
    def client_id(self) -> str:
        return self._client_id

    # ---------------------------------------------------------------- control

    def add_device(self, model: str, sn: str, *, on_dps: DpsCallback | None, on_raw: RawCallback | None = None) -> None:
        self._devices[(model, sn)] = (on_dps, on_raw)
        if self._client is not None and self.connected:
            self._subscribe(self._client, model, sn)

    async def async_start(self) -> None:
        self._loop = asyncio.get_running_loop()
        ctx = await self._loop.run_in_executor(None, _build_ssl_context, self._creds)
        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=self._client_id, clean_session=True)
        client.tls_set_context(ctx)
        client.username_pw_set(self._creds.thing_name)
        client.reconnect_delay_set(1, 60)
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        client.on_message = self._on_message
        client.on_subscribe = self._on_subscribe
        self._client = client
        try:
            client.connect_async(self._creds.endpoint, MQTT_PORT, keepalive=MQTT_KEEPALIVE_S)
            client.loop_start()
        except OSError as err:
            raise EufyConnectionError(f"MQTT connect: {type(err).__name__}") from err

    async def async_wait_connected(self, timeout: float = 20.0) -> None:
        async with asyncio.timeout(timeout):
            await self._connected.wait()

    async def async_stop(self) -> None:
        self._closed = True
        if self._client is not None:
            self._client.disconnect()
            self._client.loop_stop()
            self._client = None
        self._connected.clear()

    async def async_send_dps(self, model: str, sn: str, dps: dict[str, Any]) -> None:
        """Publish a data point write to one device."""
        if self._client is None or not self.connected:
            raise EufyConnectionError("MQTT not connected")
        ts = int(time.time() * 1000)
        self._seq += 1
        inner = {"account_id": self._creds.user_id, "data": dps, "device_sn": sn, "protocol": 2, "t": ts}
        envelope = {
            "head": {
                "client_id": self._client_id,
                "cmd": 65537,
                "cmd_status": 2,
                "msg_seq": self._seq,
                "seed": "",
                "sess_id": self._client_id,
                "sign_code": 0,
                "timestamp": ts,
                "version": "1.0.0.1",
            },
            "payload": json.dumps(inner),
        }
        topic = TOPIC_CMD_REQ.format(model=model, sn=sn)
        info = self._client.publish(topic, json.dumps(envelope).encode(), qos=0)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise EufyConnectionError(f"MQTT publish failed rc={info.rc}")

    # -------------------------------------------------------------- callbacks
    # paho thread; hop to the loop with call_soon_threadsafe.

    def _subscribe(self, client: mqtt.Client, model: str, sn: str) -> None:
        topics = [(TOPIC_CMD_RES.format(model=model, sn=sn), 0), (TOPIC_BIZ_RES.format(model=model, sn=sn), 0)]
        if self.tap_requests:
            topics += [(TOPIC_CMD_REQ.format(model=model, sn=sn), 0), (TOPIC_BIZ_RES.format(model=model, sn=sn)[:-3] + "req", 0)]
        client.subscribe(topics)

    def _on_connect(self, client: mqtt.Client, _ud: Any, _flags: Any, reason: Any, _props: Any = None) -> None:
        code = getattr(reason, "value", reason)
        if code != 0:
            _LOGGER.warning("MQTT connection refused: %s", reason)
            return
        for model, sn in self._devices:
            self._subscribe(client, model, sn)
        _LOGGER.debug("MQTT connected to %s, %d device(s) subscribed", self._creds.endpoint, len(self._devices))
        self._post(self._connected.set)
        if self.on_connection_change:
            self._post(lambda: self.on_connection_change(True))  # type: ignore[misc]

    def _on_subscribe(self, _c: mqtt.Client, _ud: Any, mid: int, reasons: Any, _props: Any = None) -> None:
        codes = [getattr(r, "value", r) for r in (reasons or [])]
        if any(c >= 128 for c in codes):
            _LOGGER.warning("MQTT subscribe refused (mid %s): %s", mid, codes)
        else:
            _LOGGER.debug("MQTT subscribed (mid %s): granted %s", mid, codes)
        self.last_subscribe_codes = codes

    def _on_disconnect(self, _c: mqtt.Client, _ud: Any, _flags: Any, reason: Any, _props: Any = None) -> None:
        _LOGGER.debug("MQTT disconnected: %s", reason)
        self._post(self._connected.clear)
        if self.on_connection_change:
            self._post(lambda: self.on_connection_change(False))  # type: ignore[misc]

    def _on_message(self, _c: mqtt.Client, _ud: Any, msg: mqtt.MQTTMessage) -> None:
        parts = msg.topic.split("/")
        if len(parts) != 5:
            return
        kind, _, model, sn, direction = parts
        cbs = self._devices.get((model, sn))
        if cbs is None:
            return
        on_dps, on_raw = cbs
        payload = bytes(msg.payload)
        if on_raw is not None:
            self._post(lambda: _maybe_await(on_raw(msg.topic, payload)))
        if kind != "cmd" or direction != "res" or on_dps is None:
            return
        dps = parse_status_envelope(payload)
        if dps:
            self._post(lambda: _maybe_await(on_dps(sn, dps)))

    def _post(self, fn: Callable[[], Any]) -> None:
        if self._loop is None or self._loop.is_closed() or self._closed:
            return
        self._loop.call_soon_threadsafe(fn)


def parse_status_envelope(payload: bytes) -> dict[str, Any] | None:
    """Return the `data` dict (data points) from a cmd/.../res message, or None."""
    try:
        outer = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(outer, dict):
        return None
    inner = outer.get("payload")
    if isinstance(inner, str):
        try:
            inner = json.loads(inner)
        except ValueError:
            return None
    if not isinstance(inner, dict):
        return None
    data = inner.get("data")
    return data if isinstance(data, dict) else None


def _maybe_await(result: Any) -> None:
    if asyncio.iscoroutine(result):
        asyncio.ensure_future(result)


def new_client_suffix() -> str:
    return secrets.token_hex(4)
