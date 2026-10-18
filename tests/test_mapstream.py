"""Map stream decoding: LZ4, frame parsing, channel detection, path points."""

from __future__ import annotations

import base64
import json
import pathlib

import pytest

from eufy_omni_cloud import mapstream
from eufy_omni_cloud.codec import write_varint
from eufy_omni_cloud.mapstream import MapStream, decode_path_points, lz4_block_decompress, parse_frame
from eufy_omni_cloud.pb import stream_pb2

CAPTURES = pathlib.Path(__file__).resolve().parents[1] / "captures"


def biz_payload(channel: int, body: bytes, *, offset: int = 0, clear: int = 0, prefix: bool = True) -> bytes:
    raw = (write_varint(len(body)) + body) if prefix else body
    inner = {"protocol": 41, "t": 1, "account_id": "x", "device_sn": "SN", "app_name": "eufy_home",
             "data": {"channel_id": channel, "clear_type": clear, "data_type": 0, "offset": offset, "len": len(raw), "data": raw.hex().upper()}}
    return json.dumps({"head": {"cmd": 65537}, "payload": json.dumps(inner)}).encode()


# --------------------------------------------------------------------------- LZ4

def test_lz4_literals_and_match() -> None:
    # token 0x52: 5 literals, match len 2+4=6 at offset 5 -> "abcde" + "abcdea" ; then token 0x10: 1 literal "z"
    block = bytes([0x52]) + b"abcde" + bytes([5, 0]) + bytes([0x10]) + b"z"
    assert lz4_block_decompress(block, 12) == b"abcdeabcdeaz"


def test_lz4_long_literal_run() -> None:
    lit = bytes(range(256)) * 2  # 512 literals: 15 + 255 + 242
    block = bytes([0xF0, 255, 242]) + lit
    assert lz4_block_decompress(block, 512) == lit


def test_lz4_size_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        lz4_block_decompress(bytes([0x10]) + b"a", 5)


# --------------------------------------------------------------------------- frames

def test_parse_frame_strips_prefix_and_keeps_partial() -> None:
    f = parse_frame(biz_payload(2, b"\x08\x02"))
    assert f is not None and f.channel == 2 and f.body == b"\x08\x02" and not f.partial
    g = parse_frame(biz_payload(11, b"\x09\x08\x01\x10\x02", offset=100, prefix=False))
    assert g is not None and g.partial and g.body.startswith(b"\x09")
    assert parse_frame(b'{"head":{},"payload":"{\\"data\\":{\\"152\\":1}}"}') is None
    assert parse_frame(b"not json") is None


# --------------------------------------------------------------------------- synthetic map

def _map_message(width: int = 8, height: int = 4, *, frame: int = 0) -> stream_pb2.Map:
    m = stream_pb2.Map(frame=frame, id=2, releases=1)
    m.info.width, m.info.height, m.info.resolution = width, height, 5
    m.info.origin.x, m.info.origin.y = -100, -50
    d = m.info.docks_v2.add()
    d.type = 1
    d.pose.x, d.pose.y, d.pose.theta = -90, -45, 0
    # row y: cell x even -> FREE, odd -> OBSTACLE on the last row, else UNKNOWN
    cells = []
    for y in range(height):
        for x in range(width):
            cells.append(mapstream.PIXEL_FREE if (x % 2 == 0 and y < height - 1) else (mapstream.PIXEL_OBSTACLE if y == height - 1 else mapstream.PIXEL_UNKNOWN))
    buf = bytearray((width * height + 3) // 4)
    for i, v in enumerate(cells):
        buf[i >> 2] |= v << ((i & 3) * 2)
    m.pixels = bytes(buf)
    m.pixel_size = len(buf)  # uncompressed
    return m


def test_map_rooms_zones_and_path_from_synthetic_frames() -> None:
    s = MapStream()
    m = _map_message()
    assert s.feed(biz_payload(2, m.SerializeToString()), now=1.0)
    rm = s.map
    assert rm.has_map and rm.grid.width == 8 and rm.grid.height == 4 and rm.map_id == 2
    assert rm.pixel(0, 0) == mapstream.PIXEL_FREE and rm.pixel(1, 0) == mapstream.PIXEL_UNKNOWN and rm.pixel(3, 3) == mapstream.PIXEL_OBSTACLE
    assert rm.docks == ((-90, -45, 0),)
    assert s.channel_types[2] == "map"

    ro = stream_pb2.RoomOutline(map_id=2, releases=1, width=8, height=4, resolution=5)
    ro.origin.x, ro.origin.y = -100, -50
    ro.pixels = bytes([(1 << 2) if x < 4 else (2 << 2) for _ in range(4) for x in range(8)])
    ro.pixel_size = len(ro.pixels)
    assert s.feed(biz_payload(4, ro.SerializeToString()), now=2.0)
    assert s.map.room_ids_present() == [1, 2]
    assert s.map.room_at(-100, -50) == 1 and s.map.room_at(-70, -50) == 2 and s.map.room_at(500, 500) == 0

    rp = stream_pb2.RoomParams(map_id=2)
    r1 = rp.rooms.add(); r1.id = 1; r1.name = "Kitchen"
    r2 = rp.rooms.add(); r2.id = 2; r2.scene.type = 5
    assert s.feed(biz_payload(5, rp.SerializeToString()), now=3.0)
    assert s.map.rooms[1].label == "Kitchen" and s.map.rooms[2].label == "Living room"

    rz = stream_pb2.RestrictedZone(map_id=2, releases=1)
    w = rz.virtual_walls.add(); w.p0.x, w.p0.y, w.p1.x, w.p1.y = 0, 0, 10, 10
    q = rz.forbidden_zones.add(); q.p0.x, q.p0.y, q.p1.x, q.p1.y, q.p2.x, q.p2.y, q.p3.x, q.p3.y = 0, 0, 5, 0, 5, 5, 0, 5
    assert s.feed(biz_payload(6, rz.SerializeToString()), now=4.0)
    assert s.map.virtual_walls == (((0, 0), (10, 10)),) and len(s.map.forbidden_zones) == 1

    dd = stream_pb2.DynamicData()
    dd.cur_pose.x, dd.cur_pose.y, dd.cur_pose.theta = -80, -40, 157
    assert s.feed(biz_payload(7, dd.SerializeToString()), now=5.0)
    assert s.map.pose == (-80, -40, 157)
    assert s.feed(biz_payload(7, dd.SerializeToString()), now=6.0) is False  # unchanged

    # path: two records, byte-swapped sign-magnitude coordinates
    def rec(x: int, y: int, flags: int) -> bytes:
        def enc(v: int) -> int:
            raw = (0x8000 | -v) if v < 0 else v
            return ((raw & 0xFF) << 8) | (raw >> 8)
        p = stream_pb2.PathPoint(xy=enc(x) | (enc(y) << 16), flags=flags)
        b = p.SerializeToString()
        return write_varint(len(b)) + b
    body = rec(-165, -376, 8) + rec(-160, -370, 8 | 0x10)
    assert s.feed(biz_payload(11, body, prefix=False), now=7.0)
    assert [(p.x, p.y, p.kind, p.new_segment) for p in s.map.path] == [(-165, -376, "go_charge", False), (-160, -370, "go_charge", True)]
    # an incremental chunk appends
    assert s.feed(biz_payload(11, rec(-150, -360, 0), offset=len(body), prefix=False), now=8.0)
    assert len(s.map.path) == 3 and s.map.path[-1].kind == "sweep"

    assert s.frames_seen == 8 and s.frames_decoded >= 7
    assert s.map.updated == 8.0


def test_p_frame_merges_into_existing_map() -> None:
    s = MapStream()
    s.feed(biz_payload(2, _map_message().SerializeToString()), now=1.0)
    p = _map_message(frame=1)
    # P-frame: everything unknown except cell (1,0) now FREE
    buf = bytearray(len(p.pixels))
    buf[0] |= mapstream.PIXEL_FREE << 2
    p.pixels = bytes(buf)
    assert s.feed(biz_payload(2, p.SerializeToString()), now=2.0)
    assert s.map.pixel(1, 0) == mapstream.PIXEL_FREE and s.map.pixel(0, 0) == mapstream.PIXEL_FREE and s.map.pixel(3, 3) == mapstream.PIXEL_OBSTACLE


def test_new_map_id_resets_rooms() -> None:
    s = MapStream()
    s.feed(biz_payload(2, _map_message().SerializeToString()), now=1.0)
    rp = stream_pb2.RoomParams(map_id=2)
    r = rp.rooms.add(); r.id = 1; r.name = "A"
    s.feed(biz_payload(5, rp.SerializeToString()), now=2.0)
    other = _map_message(); other.id = 3
    s.feed(biz_payload(2, other.SerializeToString()), now=3.0)
    assert s.map.map_id == 3 and s.map.rooms == {}


def test_decode_path_points_rejects_garbage() -> None:
    assert decode_path_points(b"\xff\xff\xff") == []


# --------------------------------------------------------------------------- real capture (local only)

@pytest.mark.skipif(not any(CAPTURES.glob("map_*.raw.jsonl")) if CAPTURES.exists() else True, reason="no local capture")
def test_real_capture_decodes() -> None:
    latest = sorted(CAPTURES.glob("map_*.raw.jsonl"))[-1]
    s = MapStream()
    for line in latest.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec["topic"].startswith("biz"):
            s.feed(base64.b64decode(rec["payload"]))
    m = s.map
    assert m.has_map and m.grid.width > 50 and m.room_grid is not None
    assert m.room_ids_present() and m.rooms
    assert m.grid.resolution == 5
    # the path tail recorded while docking must land inside the map
    for p in m.path:
        assert m.grid.cell(p.x, p.y) is not None
