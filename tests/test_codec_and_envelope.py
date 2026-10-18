"""Codec round-trips, snapshot decoding from the real C28, and MQTT envelope parsing."""

from __future__ import annotations

import base64
import json
import pathlib

import pytest
from google.protobuf.json_format import MessageToDict

from eufy_omni_cloud.codec import decode, encode, read_varint, strip_length_prefix, write_varint
from eufy_omni_cloud.mqtt import parse_status_envelope
from eufy_omni_cloud.pb import (
    clean_param_pb2,
    clean_statistics_pb2,
    consumable_pb2,
    control_pb2,
    error_code_pb2,
    scene_pb2,
    station_pb2,
    work_status_pb2,
)

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def c28_dps() -> dict:
    snap = json.loads((FIXTURES / "aiot_dps_snapshot.json").read_text(encoding="utf-8"))
    return next(d for d in snap if d["device_model"] == "T211A")["dps"]


@pytest.mark.parametrize("n", [0, 1, 127, 128, 300, 16383, 16384, 2**31])
def test_varint_roundtrip(n: int) -> None:
    data = write_varint(n) + b"tail"
    value, pos = read_varint(data)
    assert value == n
    assert data[pos:] == b"tail"


def test_strip_length_prefix_only_when_it_matches() -> None:
    body = b"\x08\x01"
    assert strip_length_prefix(write_varint(len(body)) + body) == body
    assert strip_length_prefix(body) == body  # 0x08 != remaining length 1
    assert strip_length_prefix(b"") == b""


def test_encode_decode_mode_ctrl() -> None:
    req = control_pb2.ModeCtrlRequest(method=control_pb2.ModeCtrlRequest.START_GOHOME, seq=7)
    b64 = encode(req)
    raw = base64.b64decode(b64)
    assert raw[0] == len(raw) - 1  # single-byte length prefix
    back = decode(control_pb2.ModeCtrlRequest, b64)
    assert back.method == control_pb2.ModeCtrlRequest.START_GOHOME
    assert back.seq == 7


def test_c28_work_status_docked_charged() -> None:
    ws = decode(work_status_pb2.WorkStatus, c28_dps()["153"])
    assert ws.state == work_status_pb2.WorkStatus.CHARGING
    assert ws.HasField("charging")
    assert ws.charging.state == work_status_pb2.WorkStatus.Charging.DONE


def test_c28_clean_param() -> None:
    cp = decode(clean_param_pb2.CleanParamResponse, c28_dps()["154"])
    d = MessageToDict(cp, preserving_proto_field_name=True)
    assert d["clean_param"]["clean_type"]["value"] == "SWEEP_AND_MOP"
    assert d["running_clean_param"]["fan"]["suction"] == "TURBO"


def test_c28_station_statistics_consumables_error() -> None:
    dps = c28_dps()
    st = MessageToDict(decode(station_pb2.StationResponse, dps["173"]), preserving_proto_field_name=True)
    assert st["status"]["connected"] is True
    assert st["clean_water"]["value"] == 54
    stats = decode(clean_statistics_pb2.CleanStatistics, dps["167"])
    assert stats.total.clean_count == 46
    cons = decode(consumable_pb2.ConsumableResponse, dps["168"])
    assert cons.runtime.mop.duration == 30
    err = decode(error_code_pb2.ErrorCode, dps["177"])
    assert not list(err.error) and not list(err.new_code.error)  # no active error


def test_c28_scenes() -> None:
    sc = decode(scene_pb2.SceneResponse, c28_dps()["180"])
    names = [i.name for i in sc.infos]
    assert names == [f"Routine {i.id.value}" for i in sc.infos]  # fixture names are scrubbed
    assert any(i.valid for i in sc.infos)


def test_scalars_untouched() -> None:
    dps = c28_dps()
    assert dps["163"] == 100
    assert dps["161"] == 80
    assert dps["158"] == "2"


def test_parse_status_envelope_string_payload() -> None:
    inner = {"account_id": "u", "device_sn": "sn", "protocol": 2, "t": 1, "data": {"163": 97, "153": "AA=="}}
    outer = {"head": {"cmd": 65537}, "payload": json.dumps(inner)}
    assert parse_status_envelope(json.dumps(outer).encode()) == {"163": 97, "153": "AA=="}


def test_parse_status_envelope_rejects_garbage() -> None:
    assert parse_status_envelope(b"\x00\x01") is None
    assert parse_status_envelope(b"[]") is None
    assert parse_status_envelope(json.dumps({"payload": "not json"}).encode()) is None
    assert parse_status_envelope(json.dumps({"payload": {"data": 5}}).encode()) is None
