"""State model from the real C28 snapshot, and command builders decoded back."""

from __future__ import annotations

import json
import pathlib

from eufy_omni_cloud import commands
from eufy_omni_cloud.codec import decode
from eufy_omni_cloud.const import Dp
from eufy_omni_cloud.pb import clean_param_pb2, control_pb2, work_status_pb2
from eufy_omni_cloud.codec import encode
from eufy_omni_cloud.state import Activity, DockActivity, VacuumSnapshot, apply_dps

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def snapshot_for(model: str) -> VacuumSnapshot:
    snap = json.loads((FIXTURES / "aiot_dps_snapshot.json").read_text(encoding="utf-8"))
    dps = next(d for d in snap if d["device_model"] == model)["dps"]
    dps = {k: v for k, v in dps.items() if not (isinstance(v, str) and v.startswith("<dropped"))}
    return apply_dps(VacuumSnapshot(), dps, now=1.0)


def test_c28_snapshot() -> None:
    s = snapshot_for("T211A")
    assert s.activity == Activity.DOCKED and s.docked
    assert s.charging is False and s.charge_done is True
    assert s.battery == 100
    assert s.fan_speed == "turbo" and s.running_fan == "turbo"
    assert s.clean_type == "sweep_and_mop" and s.mop_level == "middle" and s.clean_extent == "normal"
    assert s.dock_connected is True and s.dock_clean_water == 54 and s.dock_detergent is True
    assert s.error_codes == () and not s.has_error
    assert s.total_clean_count == 46 and s.last_clean_area == 56
    assert s.consumable_hours["mop"] == 30 and s.consumable_hours["side_brush"] == 47
    assert s.dnd_enabled is True
    assert s.ai_obstacle is True and s.wifi_signal == 34
    assert len(s.scenes) == 7 and {sc.name for sc in s.scenes} >= {"Routine 7", "Routine 9"}
    assert [sc.id for sc in s.scenes if sc.valid] == [7, 8, 9, 10]  # fixture routine names are generic
    assert s.volume == 80 and s.find_robot is False
    assert s.dock_activity == DockActivity.IDLE
    assert s.last_update == 1.0


def test_x10_snapshot_decodes_too() -> None:
    s = snapshot_for("T2351")
    assert s.activity == Activity.DOCKED
    assert s.battery == 100
    assert s.total_clean_count is not None


def test_push_update_only_touches_sent_points() -> None:
    s = snapshot_for("T211A")
    s2 = apply_dps(s, {Dp.BATTERY: 42}, now=2.0)
    assert s2.battery == 42 and s2.activity == Activity.DOCKED and s2.scenes == s.scenes
    assert s2.raw_dps[Dp.BATTERY] == 42 and s2.last_update == 2.0


def test_cleaning_and_paused_mapping() -> None:
    ws = work_status_pb2.WorkStatus(state=work_status_pb2.WorkStatus.CLEANING)
    ws.cleaning.state = work_status_pb2.WorkStatus.Cleaning.PAUSED
    s = apply_dps(VacuumSnapshot(), {Dp.WORK_STATUS: encode(ws)})
    assert s.activity == Activity.PAUSED and s.cleaning_paused
    ws.cleaning.state = 0
    s = apply_dps(VacuumSnapshot(), {Dp.WORK_STATUS: encode(ws)})
    assert s.activity == Activity.CLEANING
    ws2 = work_status_pb2.WorkStatus(state=work_status_pb2.WorkStatus.GO_HOME)
    assert apply_dps(VacuumSnapshot(), {Dp.WORK_STATUS: encode(ws2)}).activity == Activity.RETURNING


def test_undecodable_point_is_kept_raw() -> None:
    s = apply_dps(VacuumSnapshot(), {Dp.WORK_STATUS: "!!!notbase64", Dp.BATTERY: 5})
    assert s.battery == 5 and s.activity == Activity.UNKNOWN


def _mode(dps: dict) -> control_pb2.ModeCtrlRequest:
    return decode(control_pb2.ModeCtrlRequest, dps[Dp.PLAY_PAUSE])


def test_mode_commands() -> None:
    m = _mode(commands.start_auto_clean())
    assert m.method == control_pb2.ModeCtrlRequest.START_AUTO_CLEAN and m.auto_clean.clean_times == 1
    assert _mode(commands.pause()).method == control_pb2.ModeCtrlRequest.PAUSE_TASK
    assert _mode(commands.resume()).method == control_pb2.ModeCtrlRequest.RESUME_TASK
    assert _mode(commands.stop()).method == control_pb2.ModeCtrlRequest.STOP_TASK
    assert _mode(commands.return_to_dock()).method == control_pb2.ModeCtrlRequest.START_GOHOME
    sc = _mode(commands.start_scene(7))
    assert sc.method == control_pb2.ModeCtrlRequest.START_SCENE_CLEAN and sc.scene_clean.scene_id == 7
    rooms = _mode(commands.start_rooms([3, 5], map_id=2))
    assert [r.id for r in rooms.select_rooms_clean.rooms] == [3, 5]
    assert rooms.select_rooms_clean.map_id == 2
    # seq increments
    assert _mode(commands.pause()).seq < _mode(commands.pause()).seq


def test_scalar_and_param_commands() -> None:
    assert commands.find_robot() == {Dp.FIND_ROBOT: True}
    assert commands.set_volume(150) == {Dp.VOLUME: 100}
    assert commands.set_fan_speed("max") == {Dp.CLEAN_SPEED: 3}
    req = decode(clean_param_pb2.CleanParamRequest, commands.set_clean_type("mop_only")[Dp.CLEAN_PARAM])
    assert req.clean_param.clean_type.value == clean_param_pb2.CleanType.MOP_ONLY
    assert req.area_clean_param.clean_type.value == clean_param_pb2.CleanType.MOP_ONLY
    req = decode(clean_param_pb2.CleanParamRequest, commands.set_mop_level("high")[Dp.CLEAN_PARAM])
    assert req.clean_param.mop_mode.level == clean_param_pb2.MopMode.HIGH


def test_robot_naming() -> None:
    from eufy_omni_cloud.account import RobotVacuum

    class _Acct:
        aliases: dict[str, str] = {}
        push_connected = False

    snap = json.loads((FIXTURES / "aiot_dps_snapshot.json").read_text(encoding="utf-8"))
    dps = {k: v for k, v in snap[0]["dps"].items() if not (isinstance(v, str) and v.startswith("<dropped"))}
    rec = {"device_sn": "SN0001", "device_model": "T211A", "device_name": "Robovac", "dps": dps}
    acct = _Acct()
    assert RobotVacuum(acct, rec).name == "Eufy T211A"  # dp 169 dropped from fixtures, so falls to model
    acct.aliases = {"SN0001": "Jorge"}
    assert RobotVacuum(acct, rec).name == "Jorge"
    rec["device_name"] = "Kitchen bot"
    acct.aliases = {}
    assert RobotVacuum(acct, rec).name == "Kitchen bot"
