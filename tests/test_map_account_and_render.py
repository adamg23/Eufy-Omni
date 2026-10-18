"""Map frames reach the right robot, listeners fire, and the renderer produces a PNG."""

from __future__ import annotations

import asyncio
import io
import json

import pytest
from PIL import Image

from eufy_omni_cloud import commands
from eufy_omni_cloud.account import EufyAccount, RobotVacuum
from eufy_omni_cloud.codec import decode
from eufy_omni_cloud.maprender import render_png
from eufy_omni_cloud.mapstream import RobotMap
from eufy_omni_cloud.pb import app_device_info_pb2, keepalive_pb2, stream_pb2
from tests.test_mapstream import _map_message, biz_payload


class _Acct:
    aliases: dict[str, str] = {}
    push_connected = False
    user_id = "user-1"
    sent: list[dict] = []

    def schedule_map_request(self, robot: RobotVacuum, delay: float = 0) -> None:
        self.sent.append({"scheduled": robot.sn})

    async def async_send(self, robot: RobotVacuum, dps: dict) -> None:
        self.sent.append(dps)


def _robot(acct: _Acct) -> RobotVacuum:
    return RobotVacuum(acct, {"device_sn": "SN0001", "device_model": "T211A", "device_name": "Robovac", "dps": {}})


def test_map_frame_updates_robot_and_notifies_listeners() -> None:
    acct = _Acct()
    robot = _robot(acct)
    seen: list[int] = []
    robot.add_map_listener(lambda r: seen.append(r.map.map_id))
    robot.apply_map_frame(biz_payload(2, _map_message().SerializeToString()))
    assert robot.map.has_map and seen == [2]
    robot.apply_map_frame(b"garbage")  # ignored, no exception, no notification
    assert seen == [2]


def test_account_routes_biz_frames_by_serial() -> None:
    loop = asyncio.new_event_loop()
    try:
        acct = EufyAccount("u", "p", session=None)  # type: ignore[arg-type]
        acct.robots["SN0001"] = RobotVacuum(acct, {"device_sn": "SN0001", "device_model": "T211A", "dps": {}})
        acct._on_raw("biz/eufy_home/T211A/SN0001/res", biz_payload(2, _map_message().SerializeToString()))
        assert acct.robots["SN0001"].map.has_map
        acct._on_raw("biz/eufy_home/T211A/OTHER/res", biz_payload(2, _map_message().SerializeToString()))
        acct._on_raw("cmd/eufy_home/T211A/SN0001/res", b"{}")
    finally:
        loop.close()


def test_request_map_sends_app_info_then_keepalive() -> None:
    acct = _Acct()
    acct.sent = []
    robot = _robot(acct)
    asyncio.run(robot.async_request_map(min_interval=0))
    assert [list(d) for d in acct.sent] == [["169"], ["153"]]
    info = decode(app_device_info_pb2.AppInfo, acct.sent[0]["169"])
    assert info.user_id == "user-1" and info.app_function.optimization.options == 14
    ka = decode(keepalive_pb2.KeepAliveRequest, acct.sent[1]["153"])
    assert ka.force_sync and ka.timestamp > 1_700_000_000_000_000  # microseconds
    acct.sent = []
    asyncio.run(robot.async_request_map())  # rate limited
    assert acct.sent == []


def test_start_of_cleaning_schedules_a_map_request() -> None:
    acct = _Acct()
    acct.sent = []
    robot = _robot(acct)
    from eufy_omni_cloud.codec import encode
    from eufy_omni_cloud.pb import work_status_pb2

    ws = work_status_pb2.WorkStatus(state=work_status_pb2.WorkStatus.CLEANING)
    robot.apply_push({"153": encode(ws)})
    assert acct.sent == [{"scheduled": "SN0001"}]
    robot.apply_push({"163": 50})  # still cleaning: no second request
    assert len(acct.sent) == 1


def test_render_png_dimensions_and_markers() -> None:
    from eufy_omni_cloud.mapstream import MapStream

    s = MapStream()
    s.feed(biz_payload(2, _map_message(16, 8).SerializeToString()), now=1.0)
    dd = stream_pb2.DynamicData()
    dd.cur_pose.x, dd.cur_pose.y, dd.cur_pose.theta = -90, -40, 0
    s.feed(biz_payload(7, dd.SerializeToString()), now=2.0)
    png = render_png(s.map, max_size=160)
    img = Image.open(io.BytesIO(png))
    assert img.format == "PNG" and img.size == (160, 80)
    # dock (green) and robot (orange) are drawn
    colours = {c[1][:3] for c in img.getcolors(100000)}
    assert (40, 160, 70) in colours and (255, 140, 0) in colours


def test_render_without_map_is_a_transparent_pixel() -> None:
    img = Image.open(io.BytesIO(render_png(RobotMap())))
    assert img.size == (1, 1)


def test_keepalive_and_app_info_land_on_the_right_data_points() -> None:
    assert list(commands.keepalive(now_us=5)) == ["153"]
    assert list(commands.app_info("x")) == ["169"]
