"""Decoded, immutable view of one robot built from its data points."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import Any

from google.protobuf.message import DecodeError

from .codec import decode
from .const import Dp
from .pb import (
    app_device_info_pb2,
    clean_param_pb2,
    clean_statistics_pb2,
    consumable_pb2,
    error_code_pb2,
    scene_pb2,
    station_pb2,
    undisturbed_pb2,
    unisetting_pb2,
    work_status_pb2,
)

_LOGGER = logging.getLogger(__name__)

WorkStatus = work_status_pb2.WorkStatus
FAN_SPEEDS: tuple[str, ...] = ("quiet", "standard", "turbo", "max", "max_plus")
CLEAN_TYPES: tuple[str, ...] = ("sweep_only", "mop_only", "sweep_and_mop", "sweep_then_mop")
MOP_LEVELS: tuple[str, ...] = ("low", "middle", "high")
CLEAN_EXTENTS: tuple[str, ...] = ("normal", "narrow", "quick")
CONSUMABLES: tuple[str, ...] = (
    "side_brush",
    "rolling_brush",
    "filter_mesh",
    "scrape",
    "sensor",
    "mop",
    "dustbag",
    "dirty_waterfilter",
)


class Activity(StrEnum):
    IDLE = "idle"
    CLEANING = "cleaning"
    PAUSED = "paused"
    RETURNING = "returning"
    DOCKED = "docked"
    ERROR = "error"
    MAPPING = "mapping"
    REMOTE_CONTROL = "remote_control"
    UNKNOWN = "unknown"


class DockActivity(StrEnum):
    IDLE = "idle"
    WASHING = "washing"
    DRYING = "drying"
    COLLECTING_DUST = "collecting_dust"
    ADDING_WATER = "adding_water"
    RECYCLING_WATER = "recycling_water"


@dataclass(frozen=True)
class Scene:
    id: int
    name: str
    valid: bool
    map_id: int | None
    kind: str


@dataclass(frozen=True)
class VacuumSnapshot:
    raw_dps: dict[str, Any] = field(default_factory=dict, repr=False)
    # work status (dp 153)
    work_state: int | None = None
    activity: Activity = Activity.UNKNOWN
    charging: bool | None = None  # actively charging (not "done")
    charge_done: bool | None = None
    cleaning_paused: bool = False
    work_mode: int | None = None
    trigger_source: int | None = None
    dock_activity: DockActivity = DockActivity.IDLE
    # scalars
    battery: int | None = None
    fan_speed: str | None = None  # one of FAN_SPEEDS
    volume: int | None = None
    find_robot: bool | None = None
    multi_map: bool | None = None
    # clean parameters (dp 154)
    clean_type: str | None = None
    mop_level: str | None = None
    clean_extent: str | None = None
    running_fan: str | None = None
    # dock (dp 173)
    dock_connected: bool | None = None
    dock_clean_water: int | None = None
    dock_detergent: bool | None = None
    dock_dry_level: str | None = None
    dock_wash_mode: str | None = None
    dock_dust_collect: bool | None = None
    # errors (dp 177)
    error_codes: tuple[int, ...] = ()
    warning_codes: tuple[int, ...] = ()
    # statistics (dp 167)
    last_clean_area: int | None = None
    last_clean_duration: int | None = None
    total_clean_area: int | None = None
    total_clean_duration: int | None = None
    total_clean_count: int | None = None
    # consumables (dp 168) hours used
    consumable_hours: dict[str, int] = field(default_factory=dict)
    # misc
    dnd_enabled: bool | None = None
    child_lock: bool | None = None
    ai_obstacle: bool | None = None
    wifi_signal: int | None = None
    scenes: tuple[Scene, ...] = ()
    product_name: str | None = None
    firmware: str | None = None
    station_firmware: str | None = None
    online: bool | None = None
    push_connected: bool = False
    last_update: float | None = None

    @property
    def has_error(self) -> bool:
        return bool(self.error_codes)

    @property
    def docked(self) -> bool:
        return self.activity == Activity.DOCKED


def _enum_name(names: tuple[str, ...], index: int | None) -> str | None:
    if index is None or not 0 <= index < len(names):
        return None
    return names[index]


def _activity(ws: Any) -> tuple[Activity, DockActivity, bool]:
    """Map WorkStatus to (activity, dock activity, paused)."""
    s = ws.state
    paused = ws.HasField("cleaning") and ws.cleaning.state == WorkStatus.Cleaning.PAUSED
    dock = DockActivity.IDLE
    if ws.HasField("station"):
        st = ws.station
        if st.HasField("washing_drying_system"):
            dock = DockActivity.DRYING if st.washing_drying_system.state == 1 else DockActivity.WASHING
        elif st.HasField("dust_collection_system"):
            dock = DockActivity.COLLECTING_DUST
        elif st.HasField("water_injection_system"):
            dock = DockActivity.ADDING_WATER
    if s in (WorkStatus.STANDBY, WorkStatus.SLEEP):
        return Activity.IDLE, dock, paused
    if s == WorkStatus.FAULT:
        return Activity.ERROR, dock, paused
    if s == WorkStatus.CHARGING:
        return Activity.DOCKED, dock, paused
    if s == WorkStatus.FAST_MAPPING:
        return Activity.MAPPING, dock, paused
    if s == WorkStatus.CLEANING:
        if ws.HasField("go_wash") and ws.go_wash.mode in (1, 2):
            return Activity.DOCKED, (dock if dock != DockActivity.IDLE else DockActivity.WASHING), paused
        if dock in (DockActivity.WASHING, DockActivity.DRYING):
            return Activity.DOCKED, dock, paused
        return (Activity.PAUSED if paused else Activity.CLEANING), dock, paused
    if s == WorkStatus.REMOTE_CTRL:
        return Activity.REMOTE_CONTROL, dock, paused
    if s == WorkStatus.GO_HOME:
        return Activity.RETURNING, dock, paused
    if s == WorkStatus.CRUISIING:
        return Activity.CLEANING, dock, paused
    return Activity.UNKNOWN, dock, paused


def _scene_kind(info: Any) -> str:
    enum = info.DESCRIPTOR.fields_by_name["type"].enum_type
    if enum is not None and info.type in enum.values_by_number:
        return enum.values_by_number[info.type].name.lower()
    return str(info.type)


def _decode(msg_type: Any, value: Any, dp: str) -> Any | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return decode(msg_type, value)
    except (DecodeError, ValueError, TypeError) as err:
        _LOGGER.debug("dp %s did not decode as %s: %s", dp, msg_type.__name__, err)
        return None


def apply_dps(prev: VacuumSnapshot, dps: dict[str, Any], *, now: float | None = None) -> VacuumSnapshot:
    """Return a new snapshot with `dps` folded into `prev`. Unknown or undecodable points are kept raw."""
    ch: dict[str, Any] = {}
    raw = dict(prev.raw_dps)
    raw.update(dps)
    ch["raw_dps"] = raw
    ch["last_update"] = now if now is not None else time.time()

    if Dp.BATTERY in dps and isinstance(dps[Dp.BATTERY], int):
        ch["battery"] = dps[Dp.BATTERY]
    if Dp.VOLUME in dps and isinstance(dps[Dp.VOLUME], int):
        ch["volume"] = dps[Dp.VOLUME]
    if Dp.FIND_ROBOT in dps and isinstance(dps[Dp.FIND_ROBOT], bool):
        ch["find_robot"] = dps[Dp.FIND_ROBOT]
    if Dp.MULTI_MAP_SWITCH in dps and isinstance(dps[Dp.MULTI_MAP_SWITCH], bool):
        ch["multi_map"] = dps[Dp.MULTI_MAP_SWITCH]
    if Dp.CLEAN_SPEED in dps:
        v = dps[Dp.CLEAN_SPEED]
        idx = int(v) if isinstance(v, int) or (isinstance(v, str) and v.isdigit()) else None
        ch["fan_speed"] = _enum_name(FAN_SPEEDS, idx)

    if (ws := _decode(WorkStatus, dps.get(Dp.WORK_STATUS), Dp.WORK_STATUS)) is not None:
        activity, dock, paused = _activity(ws)
        ch.update(
            work_state=ws.state,
            activity=activity,
            dock_activity=dock,
            cleaning_paused=paused,
            work_mode=ws.mode.value if ws.HasField("mode") else None,
            trigger_source=ws.trigger.source if ws.HasField("trigger") else None,
        )
        if ws.HasField("charging"):
            ch["charging"] = ws.charging.state == WorkStatus.Charging.DOING
            ch["charge_done"] = ws.charging.state == WorkStatus.Charging.DONE
        else:
            ch["charging"] = False
            ch["charge_done"] = None

    if (cp := _decode(clean_param_pb2.CleanParamResponse, dps.get(Dp.CLEAN_PARAM), Dp.CLEAN_PARAM)) is not None:
        p = cp.clean_param
        ch["clean_type"] = _enum_name(CLEAN_TYPES, p.clean_type.value if p.HasField("clean_type") else None)
        ch["mop_level"] = _enum_name(MOP_LEVELS, p.mop_mode.level if p.HasField("mop_mode") else None)
        ch["clean_extent"] = _enum_name(CLEAN_EXTENTS, p.clean_extent.value if p.HasField("clean_extent") else None)
        rp = cp.running_clean_param
        ch["running_fan"] = _enum_name(FAN_SPEEDS, rp.fan.suction if rp.HasField("fan") else None)

    if (st := _decode(station_pb2.StationResponse, dps.get(Dp.STATION), Dp.STATION)) is not None:
        if st.HasField("status"):
            ch["dock_connected"] = st.status.connected
        if st.HasField("clean_water"):
            ch["dock_clean_water"] = st.clean_water.value
        if st.HasField("auto_cfg_status"):
            cfg = st.auto_cfg_status
            ch["dock_detergent"] = bool(cfg.detergent)
            if cfg.HasField("dry"):
                ch["dock_dry_level"] = cfg.dry.duration.level if cfg.dry.HasField("duration") else None
            if cfg.HasField("wash"):
                ch["dock_wash_mode"] = cfg.wash.wash_freq.mode if cfg.wash.HasField("wash_freq") else None
            if cfg.HasField("collectdust_v2"):
                ch["dock_dust_collect"] = cfg.collectdust_v2.sw.value if cfg.collectdust_v2.HasField("sw") else None

    if (ec := _decode(error_code_pb2.ErrorCode, dps.get(Dp.ERROR_CODE), Dp.ERROR_CODE)) is not None:
        ch["error_codes"] = tuple(ec.error) or tuple(ec.new_code.error)
        ch["warning_codes"] = tuple(ec.warn) or tuple(ec.new_code.warn)

    if (cs := _decode(clean_statistics_pb2.CleanStatistics, dps.get(Dp.CLEAN_STATISTICS), Dp.CLEAN_STATISTICS)) is not None:
        ch.update(
            last_clean_area=cs.single.clean_area,
            last_clean_duration=cs.single.clean_duration,
            total_clean_area=cs.total.clean_area,
            total_clean_duration=cs.total.clean_duration,
            total_clean_count=cs.total.clean_count,
        )

    if (co := _decode(consumable_pb2.ConsumableResponse, dps.get(Dp.CONSUMABLES), Dp.CONSUMABLES)) is not None and co.HasField("runtime"):
        hours = dict(prev.consumable_hours)
        for name in CONSUMABLES:
            if co.runtime.HasField(name):
                hours[name] = getattr(co.runtime, name).duration
        ch["consumable_hours"] = hours

    if (un := _decode(undisturbed_pb2.UndisturbedResponse, dps.get(Dp.UNDISTURBED), Dp.UNDISTURBED)) is not None and un.HasField("undisturbed"):
        ch["dnd_enabled"] = un.undisturbed.sw.value if un.undisturbed.HasField("sw") else False

    if (us := _decode(unisetting_pb2.UnisettingResponse, dps.get(Dp.UNISETTING), Dp.UNISETTING)) is not None:
        ch["child_lock"] = us.children_lock.value if us.HasField("children_lock") else False
        ch["ai_obstacle"] = us.ai_see.value if us.HasField("ai_see") else None
        ch["wifi_signal"] = us.ap_signal_strength or None

    if (sc := _decode(scene_pb2.SceneResponse, dps.get(Dp.SCENE), Dp.SCENE)) is not None and sc.infos:
        ch["scenes"] = tuple(
            Scene(
                id=i.id.value,
                name=i.name,
                valid=bool(i.valid),
                map_id=i.mapid if i.mapid < 0xFFFFFFF0 else None,
                kind=_scene_kind(i),
            )
            for i in sc.infos
        )

    if (di := _decode(app_device_info_pb2.DeviceInfo, dps.get(Dp.DEVICE_INFO), Dp.DEVICE_INFO)) is not None:
        # Only the non-identifying parts are kept; MAC, SSID, IP and user id stay out of the snapshot.
        ch["product_name"] = di.product_name or None
        ch["firmware"] = di.software or None
        ch["station_firmware"] = di.station.software or None if di.HasField("station") else None

    return replace(prev, **ch)
