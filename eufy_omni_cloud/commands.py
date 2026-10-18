"""Data point writes. Each builder returns the `data` dict to publish."""

from __future__ import annotations

from itertools import count
from typing import Any

from .codec import encode
from .const import Dp
from .pb import clean_param_pb2, consumable_pb2, control_pb2
from .state import CLEAN_EXTENTS, CLEAN_TYPES, FAN_SPEEDS, MOP_LEVELS

ModeCtrlRequest = control_pb2.ModeCtrlRequest
_seq = count(1)


def _mode_ctrl(method: int, **fields: Any) -> dict[str, Any]:
    req = ModeCtrlRequest(method=method, seq=next(_seq), **fields)
    return {Dp.PLAY_PAUSE: encode(req)}


def start_auto_clean(clean_times: int = 1) -> dict[str, Any]:
    return _mode_ctrl(
        ModeCtrlRequest.START_AUTO_CLEAN,
        auto_clean=control_pb2.AutoClean(clean_times=clean_times, force_mapping=False),
    )


def pause() -> dict[str, Any]:
    return _mode_ctrl(ModeCtrlRequest.PAUSE_TASK)


def resume() -> dict[str, Any]:
    return _mode_ctrl(ModeCtrlRequest.RESUME_TASK)


def stop() -> dict[str, Any]:
    return _mode_ctrl(ModeCtrlRequest.STOP_TASK)


def return_to_dock() -> dict[str, Any]:
    return _mode_ctrl(ModeCtrlRequest.START_GOHOME)


def go_wash_mop() -> dict[str, Any]:
    return _mode_ctrl(ModeCtrlRequest.START_GOWASH)


def start_scene(scene_id: int) -> dict[str, Any]:
    return _mode_ctrl(ModeCtrlRequest.START_SCENE_CLEAN, scene_clean=control_pb2.SceneClean(scene_id=scene_id))


def start_rooms(room_ids: list[int], map_id: int, clean_times: int = 1) -> dict[str, Any]:
    rooms = control_pb2.SelectRoomsClean(
        rooms=[control_pb2.SelectRoomsClean.Room(id=rid, order=i + 1) for i, rid in enumerate(room_ids)],
        mode=control_pb2.SelectRoomsClean.GENERAL,
        clean_times=clean_times,
        map_id=map_id,
    )
    return _mode_ctrl(ModeCtrlRequest.START_SELECT_ROOMS_CLEAN, select_rooms_clean=rooms)


def find_robot(active: bool = True) -> dict[str, Any]:
    return {Dp.FIND_ROBOT: bool(active)}


def set_volume(percent: int) -> dict[str, Any]:
    return {Dp.VOLUME: max(0, min(100, int(percent)))}


def set_fan_speed(speed: str) -> dict[str, Any]:
    if speed not in FAN_SPEEDS:
        raise ValueError(f"fan speed must be one of {FAN_SPEEDS}")
    return {Dp.CLEAN_SPEED: FAN_SPEEDS.index(speed)}


def _clean_param(**fields: Any) -> dict[str, Any]:
    param = clean_param_pb2.CleanParam(**fields)
    req = clean_param_pb2.CleanParamRequest(clean_param=param, area_clean_param=param)
    return {Dp.CLEAN_PARAM: encode(req)}


def set_clean_type(name: str) -> dict[str, Any]:
    if name not in CLEAN_TYPES:
        raise ValueError(f"clean type must be one of {CLEAN_TYPES}")
    return _clean_param(clean_type=clean_param_pb2.CleanType(value=CLEAN_TYPES.index(name)))


def set_mop_level(name: str) -> dict[str, Any]:
    if name not in MOP_LEVELS:
        raise ValueError(f"mop level must be one of {MOP_LEVELS}")
    return _clean_param(mop_mode=clean_param_pb2.MopMode(level=MOP_LEVELS.index(name)))


def set_clean_extent(name: str) -> dict[str, Any]:
    if name not in CLEAN_EXTENTS:
        raise ValueError(f"clean extent must be one of {CLEAN_EXTENTS}")
    return _clean_param(clean_extent=clean_param_pb2.CleanExtent(value=CLEAN_EXTENTS.index(name)))


def reset_consumable(reset_type: int) -> dict[str, Any]:
    return {Dp.CONSUMABLES: encode(consumable_pb2.ConsumableRequest(reset_types=[reset_type]))}


# ----------------------------------------------------------------- map stream wake-up
# What the phone app sends when its map screen opens (captured 2026-10-17): first an
# AppInfo on dp 169 saying who is asking, then a KeepAliveRequest on dp 153 whose
# timestamp is in *microseconds*; with force_sync set the robot streams every map
# channel (map, rooms, zones, path) on biz/.../res even while docked.

def app_info(user_id: str, *, app_version: str = "6.1.11") -> dict[str, Any]:
    from .pb import app_device_info_pb2

    info = app_device_info_pb2.AppInfo(
        platform=app_device_info_pb2.AppInfo.PF_ANDROID,
        app_version=app_version,
        user_id=user_id,
        data_center=app_device_info_pb2.AppInfo.AZ,
    )
    info.app_function.multi_maps.version = 1
    info.app_function.multi_maps.options = 1
    info.app_function.optimization.version = 1
    info.app_function.optimization.options = 14
    return {Dp.DEVICE_INFO: encode(info)}


def keepalive(*, force_sync: bool = True, now_us: int | None = None) -> dict[str, Any]:
    import time

    from .pb import keepalive_pb2

    req = keepalive_pb2.KeepAliveRequest(timestamp=now_us or int(time.time() * 1_000_000), force_sync=force_sync)
    return {Dp.WORK_STATUS: encode(req)}
