"""High-level API: one Eufy account, its robots, push updates and commands."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable
from typing import Any

import aiohttp

from . import commands
from .exceptions import EufyAuthError, EufyCloudError, EufyConnectionError
from .http import EufyCloudHttp, MqttCredentials, Session, new_openudid
from .mapstream import MapStream, RobotMap
from .mqtt import EufyMqtt
from .state import VacuumSnapshot, apply_dps

_LOGGER = logging.getLogger(__name__)

Listener = Callable[["RobotVacuum"], None]
MAP_REQUEST_DELAY_S = 3.0


def _is_protobuf_device(dps: dict[str, Any]) -> bool:
    v = dps.get("153")
    return isinstance(v, str) and not v.isdigit()


class RobotVacuum:
    """One robot on the account. Snapshot is replaced (never mutated) on every update."""

    def __init__(self, account: EufyAccount, record: dict[str, Any]) -> None:
        self._account = account
        self.sn: str = record["device_sn"]
        self.model: str = record.get("device_model") or "unknown"
        self.name: str = record.get("device_name") or record.get("alias_name") or f"Eufy {self.model}"
        self.firmware: str | None = record.get("main_sw_version")
        self.snapshot = VacuumSnapshot()
        self._listeners: list[Listener] = []
        self.map_stream = MapStream()
        self._map_listeners: list[Listener] = []
        self._last_map_request = 0.0
        self.update_from_record(record)
        self.name = self._pick_name(record, account.aliases.get(self.sn))

    def _pick_name(self, record: dict[str, Any], alias: str | None) -> str:
        """Eufy names every robot "Robovac" by default; prefer the user's alias, then the product name."""
        device_name = record.get("alias_name") or record.get("device_name") or ""
        if alias and alias.strip():
            return alias.strip()
        if device_name and device_name.strip().lower() not in ("robovac", "eufy robovac", "robot vacuum"):
            return device_name.strip()
        if self.snapshot.product_name:
            return self.snapshot.product_name
        return f"Eufy {self.model}"

    def __repr__(self) -> str:
        return f"RobotVacuum(model={self.model!r}, sn=…{self.sn[-4:]}, activity={self.snapshot.activity})"

    # ------------------------------------------------------------- updates

    def update_from_record(self, record: dict[str, Any]) -> None:
        dps = record.get("dps") or {}
        online = record.get("device_status")
        snap = apply_dps(self.snapshot, dps) if dps else self.snapshot
        self.snapshot = snap.__class__(**{**snap.__dict__, "online": (online == 1) if online is not None else snap.online, "push_connected": self._account.push_connected})
        self.firmware = record.get("main_sw_version") or self.firmware
        self._notify()

    def apply_push(self, dps: dict[str, Any]) -> None:
        was_cleaning = self.snapshot.activity in ("cleaning", "returning", "mapping")
        snap = apply_dps(self.snapshot, dps)
        self.snapshot = snap.__class__(**{**snap.__dict__, "push_connected": True, "online": True})
        self._notify()
        if not was_cleaning and self.snapshot.activity in ("cleaning", "mapping"):
            # a run just started: the robot streams path/pose on its own, but ask for the
            # full map so the picture starts from a known state
            self._account.schedule_map_request(self)

    @property
    def map(self) -> RobotMap:
        return self.map_stream.map

    def apply_map_frame(self, payload: bytes) -> None:
        """One raw biz/ frame from MQTT."""
        try:
            changed = self.map_stream.feed(payload)
        except Exception:  # noqa: BLE001 - never let a bad frame kill the MQTT callback
            _LOGGER.exception("map frame failed")
            return
        if changed:
            for cb in list(self._map_listeners):
                try:
                    cb(self)
                except Exception:  # noqa: BLE001
                    _LOGGER.exception("map listener failed")

    def add_map_listener(self, cb: Listener) -> Callable[[], None]:
        self._map_listeners.append(cb)
        return lambda: self._map_listeners.remove(cb)

    async def async_request_map(self, *, min_interval: float = 5.0) -> None:
        """Ask the robot to stream its map now (what the app does when its map opens)."""
        now = time.monotonic()
        if now - self._last_map_request < min_interval:
            return
        self._last_map_request = now
        user_id = self._account.user_id
        if user_id:
            await self.async_send(commands.app_info(user_id))
            await asyncio.sleep(0.5)
        await self.async_send(commands.keepalive(force_sync=True))

    def set_push_connected(self, connected: bool) -> None:
        if self.snapshot.push_connected != connected:
            self.snapshot = self.snapshot.__class__(**{**self.snapshot.__dict__, "push_connected": connected})
            self._notify()

    def add_listener(self, cb: Listener) -> Callable[[], None]:
        self._listeners.append(cb)
        return lambda: self._listeners.remove(cb)

    def _notify(self) -> None:
        for cb in list(self._listeners):
            try:
                cb(self)
            except Exception:  # noqa: BLE001
                _LOGGER.exception("listener failed")

    # ------------------------------------------------------------ commands

    async def async_send(self, dps: dict[str, Any]) -> None:
        await self._account.async_send(self, dps)

    async def async_start(self) -> None:
        if self.snapshot.cleaning_paused:
            await self.async_send(commands.resume())
        else:
            await self.async_send(commands.start_auto_clean())

    async def async_pause(self) -> None:
        await self.async_send(commands.pause())

    async def async_stop(self) -> None:
        await self.async_send(commands.stop())

    async def async_return_to_dock(self) -> None:
        await self.async_send(commands.return_to_dock())

    async def async_locate(self) -> None:
        await self.async_send(commands.find_robot(True))

    async def async_set_fan_speed(self, speed: str) -> None:
        await self.async_send(commands.set_fan_speed(speed))

    async def async_set_volume(self, percent: int) -> None:
        await self.async_send(commands.set_volume(percent))

    async def async_set_clean_type(self, name: str) -> None:
        await self.async_send(commands.set_clean_type(name))

    async def async_set_mop_level(self, name: str) -> None:
        await self.async_send(commands.set_mop_level(name))

    async def async_set_clean_extent(self, name: str) -> None:
        await self.async_send(commands.set_clean_extent(name))

    async def async_wash_mop(self) -> None:
        await self.async_send(commands.go_wash_mop())

    async def async_start_scene(self, scene_id: int) -> None:
        await self.async_send(commands.start_scene(scene_id))

    async def async_start_rooms(self, room_ids: list[int], map_id: int) -> None:
        await self.async_send(commands.start_rooms(room_ids, map_id))


class EufyAccount:
    """Login once, discover robots, keep an MQTT connection and a slow HTTP poll as safety net."""

    def __init__(
        self,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
        *,
        openudid: str | None = None,
        saved_session: dict[str, Any] | None = None,
        poll_interval: float = 300.0,
    ) -> None:
        self.openudid = openudid or new_openudid()
        self._http = EufyCloudHttp(username, password, self.openudid, session)
        if saved_session and saved_session.get("access_token"):
            self._http.session = Session(
                access_token=saved_session["access_token"],
                user_id=saved_session.get("user_id", ""),
                login_client=saved_session.get("login_client", "saved"),
                user_center_id=saved_session.get("user_center_id"),
                user_center_token=saved_session.get("user_center_token"),
            )
        self._poll_interval = poll_interval
        self._mqtt: EufyMqtt | None = None
        self._creds: MqttCredentials | None = None
        self._poll_task: asyncio.Task[None] | None = None
        self.robots: dict[str, RobotVacuum] = {}
        self.aliases: dict[str, str] = {}
        self._bg_tasks: set[asyncio.Task[None]] = set()

    @property
    def push_connected(self) -> bool:
        return self._mqtt is not None and self._mqtt.connected

    @property
    def user_id(self) -> str:
        if self._creds is not None and self._creds.user_id:
            return self._creds.user_id
        return self._http.session.user_id if self._http.session else ""

    def schedule_map_request(self, robot: RobotVacuum, delay: float = MAP_REQUEST_DELAY_S) -> None:
        """Request the robot's map shortly, from any context (also MQTT callbacks)."""
        loop = asyncio.get_event_loop()

        async def _later() -> None:
            await asyncio.sleep(delay)
            try:
                await robot.async_request_map()
            except EufyCloudError as err:
                _LOGGER.debug("map request for %s failed: %s", robot, err)

        task = loop.create_task(_later())
        self._bg_tasks.add(task)
        task.add_done_callback(self._bg_tasks.discard)

    def export_session(self) -> dict[str, Any]:
        """Tokens worth persisting so the next start does not need a fresh login."""
        s = self._http.session
        if s is None:
            return {}
        return {
            "access_token": s.access_token,
            "user_id": s.user_id,
            "login_client": s.login_client,
            "user_center_id": s.user_center_id,
            "user_center_token": s.user_center_token,
            "openudid": self.openudid,
        }

    # -------------------------------------------------------------- lifecycle

    async def async_login(self) -> None:
        """Validate the saved session or log in. Raises EufyAuthError on bad credentials."""
        if self._http.session is not None:
            try:
                await self._http.async_aiot_devices()
                return
            except EufyAuthError:
                _LOGGER.debug("saved session rejected; logging in")
        await self._http.async_login()

    async def async_discover(self) -> list[RobotVacuum]:
        records = await self._http.async_aiot_devices()
        if not self.aliases:
            try:
                for d in await self._http.async_cloud_devices():
                    key = d.get("id") or d.get("sn")
                    if key and (d.get("alias_name") or d.get("name")):
                        self.aliases[key] = d.get("alias_name") or d.get("name")
            except EufyCloudError as err:
                _LOGGER.debug("alias lookup skipped: %s", err)
        for rec in records:
            if not rec.get("device_sn") or not _is_protobuf_device(rec.get("dps") or {}):
                _LOGGER.debug("skipping non-protobuf device %s", rec.get("device_model"))
                continue
            robot = self.robots.get(rec["device_sn"])
            if robot is None:
                self.robots[rec["device_sn"]] = RobotVacuum(self, rec)
            else:
                robot.update_from_record(rec)
        return list(self.robots.values())

    async def async_connect(self) -> None:
        await self.async_login()
        await self.async_discover()
        self._creds = await self._http.async_mqtt_credentials()
        self._mqtt = EufyMqtt(self._creds, self.openudid)
        for robot in self.robots.values():
            self._mqtt.add_device(robot.model, robot.sn, on_dps=self._on_dps, on_raw=self._on_raw)
        self._mqtt.on_connection_change = self._on_connection_change
        await self._mqtt.async_start()
        try:
            await self._mqtt.async_wait_connected(20)
        except TimeoutError:
            _LOGGER.warning("MQTT not connected after 20 s; continuing with HTTP polling")
        else:
            for robot in self.robots.values():
                self.schedule_map_request(robot)
        if self._poll_task is None:
            self._poll_task = asyncio.create_task(self._poll_loop())

    async def async_refresh(self) -> None:
        """HTTP snapshot refresh for every robot."""
        try:
            await self.async_discover()
        except EufyAuthError:
            await self._http.async_login()
            await self.async_discover()

    async def async_close(self) -> None:
        if self._poll_task is not None:
            self._poll_task.cancel()
            self._poll_task = None
        for task in list(self._bg_tasks):
            task.cancel()
        if self._mqtt is not None:
            await self._mqtt.async_stop()
            self._mqtt = None
        for robot in self.robots.values():
            robot.set_push_connected(False)

    async def async_send(self, robot: RobotVacuum, dps: dict[str, Any]) -> None:
        if self._mqtt is None:
            raise EufyConnectionError("not connected")
        await self._mqtt.async_send_dps(robot.model, robot.sn, dps)

    # -------------------------------------------------------------- internals

    def _on_dps(self, sn: str, dps: dict[str, Any]) -> None:
        robot = self.robots.get(sn)
        if robot is not None:
            robot.apply_push(dps)

    def _on_raw(self, topic: str, payload: bytes) -> None:
        parts = topic.split("/")
        if len(parts) == 5 and parts[0] == "biz" and parts[4] == "res":
            robot = self.robots.get(parts[3])
            if robot is not None:
                robot.apply_map_frame(payload)

    def _on_connection_change(self, connected: bool) -> None:
        for robot in self.robots.values():
            robot.set_push_connected(connected)

    async def _poll_loop(self) -> None:
        while True:
            await asyncio.sleep(self._poll_interval)
            try:
                await self.async_refresh()
            except EufyCloudError as err:
                _LOGGER.debug("poll failed: %s", err)
            except Exception:  # noqa: BLE001
                _LOGGER.exception("poll crashed")
