"""Decoder for the robot's map stream (MQTT ``biz/.../res``, "protocol 41").

Each biz frame is a JSON envelope whose payload carries one *channel* of the map:

    {"channel_id": 2, "clear_type": 0, "data_type": 0, "offset": 0, "len": 13046,
     "data": "<hex: varint(len) + protobuf>"}

Channels observed on the Omni C28 (firmware 4.9.1), map 2:

| channel | message            | notes                                              |
|---------|--------------------|----------------------------------------------------|
| 2       | ``Map``            | 2-bit occupancy grid, LZ4 block compressed          |
| 4       | ``RoomOutline``    | 1 byte per cell: room id << 2 | cell sub-type, LZ4   |
| 5       | ``RoomParams``     | room ids, names, scene types                        |
| 6       | ``RestrictedZone`` | virtual walls, no-go and no-mop quadrangles         |
| 8       | ``TemporaryData``  | current room / zone selection                       |
| 9       | ``ObstacleInfo``   | AI-detected objects                                 |
| 11      | path               | concatenated length-delimited ``PathPoint`` records |

Channel numbers are assigned by the robot (``Metadata.ChanIds``), so this decoder
identifies each frame by content and only remembers the mapping as a hint. Nothing
here touches the network; feed it raw frame payloads with :meth:`MapStream.feed`.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field, replace
from typing import Any

from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.message import DecodeError

from .codec import read_varint
from .pb import stream_pb2

_LOGGER = logging.getLogger(__name__)

PIXEL_UNKNOWN, PIXEL_OBSTACLE, PIXEL_FREE, PIXEL_CARPET = 0, 1, 2, 3

# PathPoint.flags bit 0-3: what the robot was doing when it recorded the point.
PATH_KINDS = {
    0: "sweep", 1: "mop", 2: "sweep_mop", 3: "fast_mapping", 4: "cruising", 5: "point_to_point",
    6: "remote_ctrl", 7: "go_charge_in_work", 8: "go_charge", 9: "go_wash_in_work", 10: "go_wash",
    11: "explore_stations", 12: "navigation", 13: "resume_cleaning", 14: "return_start_point", 15: "hide",
}

ROOM_SCENE_NAMES = {1: "Study", 2: "Bedroom", 3: "Bathroom", 4: "Kitchen", 5: "Living room", 6: "Dining room", 7: "Corridor"}


# ----------------------------------------------------------------------------- LZ4

def lz4_block_decompress(data: bytes, expected_size: int) -> bytes:
    """Decode one raw LZ4 block (no frame header), as the robot's firmware emits."""
    out = bytearray()
    i, n = 0, len(data)
    while i < n:
        token = data[i]
        i += 1
        literals = token >> 4
        if literals == 15:
            while True:
                if i >= n:
                    raise ValueError("truncated LZ4 literal length")
                b = data[i]
                i += 1
                literals += b
                if b != 255:
                    break
        out += data[i : i + literals]
        i += literals
        if i >= n:
            break  # last sequence carries literals only
        if i + 1 >= n:
            raise ValueError("truncated LZ4 match offset")
        offset = data[i] | (data[i + 1] << 8)
        i += 2
        if offset == 0 or offset > len(out):
            raise ValueError("bad LZ4 match offset")
        match = (token & 15) + 4
        if (token & 15) == 15:
            while True:
                if i >= n:
                    raise ValueError("truncated LZ4 match length")
                b = data[i]
                i += 1
                match += b
                if b != 255:
                    break
        start = len(out) - offset
        if offset >= match:
            out += out[start : start + match]
        else:  # overlapping copy
            for k in range(match):
                out.append(out[start + k])
    if len(out) != expected_size:
        raise ValueError(f"LZ4 output {len(out)} B, expected {expected_size}")
    return bytes(out)


def _unpack_pixels(msg: Any) -> bytes:
    """Return the raw pixel buffer of a Map / RoomOutline, decompressing if needed."""
    raw = bytes(msg.pixels)
    if msg.pixel_size and len(raw) != msg.pixel_size:
        raw = lz4_block_decompress(raw, msg.pixel_size)
    return raw


# ----------------------------------------------------------------------------- model

@dataclass(frozen=True)
class Grid:
    """A cell grid anchored in world centimetres; cell (0, 0) is at ``origin``."""

    width: int
    height: int
    resolution: int  # cm per cell
    origin_x: int  # cm
    origin_y: int  # cm

    def cell(self, x_cm: float, y_cm: float) -> tuple[int, int] | None:
        cx = round((x_cm - self.origin_x) / self.resolution)
        cy = round((y_cm - self.origin_y) / self.resolution)
        if 0 <= cx < self.width and 0 <= cy < self.height:
            return cx, cy
        return None


@dataclass(frozen=True)
class Room:
    id: int
    name: str
    scene_type: int = 0

    @property
    def label(self) -> str:
        return self.name or ROOM_SCENE_NAMES.get(self.scene_type) or f"Room {self.id}"


@dataclass(frozen=True)
class PathPoint:
    x: int  # cm
    y: int  # cm
    kind: str
    new_segment: bool


@dataclass(frozen=True)
class RobotMap:
    """Everything known about the active map. Immutable; :class:`MapStream` replaces it."""

    map_id: int = 0
    releases: int = 0
    frame_is_full: bool = True
    grid: Grid | None = None
    pixels: bytes = b""  # 2 bits per cell, LSB first, PIXEL_* values
    docks: tuple[tuple[int, int, int], ...] = ()  # (x cm, y cm, theta)
    room_grid: Grid | None = None
    room_pixels: bytes = b""  # 1 byte per cell: room id << 2 | sub-type
    rooms: dict[int, Room] = field(default_factory=dict)
    virtual_walls: tuple[tuple[tuple[int, int], tuple[int, int]], ...] = ()
    forbidden_zones: tuple[tuple[tuple[int, int], ...], ...] = ()
    no_mop_zones: tuple[tuple[tuple[int, int], ...], ...] = ()
    path: tuple[PathPoint, ...] = ()
    pose: tuple[int, int, int] | None = None  # (x cm, y cm, theta)
    obstacles: tuple[tuple[str, int, int], ...] = ()
    updated: float = 0.0

    @property
    def has_map(self) -> bool:
        return self.grid is not None and bool(self.pixels)

    def pixel(self, cx: int, cy: int) -> int:
        if self.grid is None:
            return PIXEL_UNKNOWN
        i = cy * self.grid.width + cx
        byte = i >> 2
        if byte >= len(self.pixels):
            return PIXEL_UNKNOWN
        return (self.pixels[byte] >> ((i & 3) * 2)) & 3

    def room_at(self, x_cm: float, y_cm: float) -> int:
        """Room id at a world position, 0 if none."""
        if self.room_grid is None:
            return 0
        c = self.room_grid.cell(x_cm, y_cm)
        if c is None:
            return 0
        i = c[1] * self.room_grid.width + c[0]
        return self.room_pixels[i] >> 2 if i < len(self.room_pixels) else 0

    def room_ids_present(self) -> list[int]:
        return sorted({b >> 2 for b in self.room_pixels} - {0})


# ----------------------------------------------------------------------------- frames

@dataclass(frozen=True)
class Frame:
    channel: int
    offset: int
    length: int
    clear: int
    data_type: int
    body: bytes  # protobuf bytes with the varint length prefix removed

    @property
    def partial(self) -> bool:
        return self.offset > 0


def parse_frame(payload: bytes) -> Frame | None:
    """Parse one raw ``biz/.../res`` MQTT payload; None if it is not a map frame."""
    try:
        env = json.loads(payload)
        inner = env.get("payload")
        if isinstance(inner, str):
            inner = json.loads(inner)
        data = inner.get("data") if isinstance(inner, dict) else None
        if not isinstance(data, dict) or "channel_id" not in data:
            return None
        raw = bytes.fromhex(data.get("data", ""))
    except (ValueError, TypeError, AttributeError):
        return None
    offset = int(data.get("offset", 0) or 0)
    body = raw
    if offset == 0 and raw:
        length, pos = read_varint(raw, 0)
        if length == len(raw) - pos:
            body = raw[pos:]
    return Frame(
        channel=int(data["channel_id"]),
        offset=offset,
        length=int(data.get("len", len(raw)) or len(raw)),
        clear=int(data.get("clear_type", 0) or 0),
        data_type=int(data.get("data_type", 0) or 0),
        body=body,
    )


def decode_path_points(body: bytes) -> list[PathPoint]:
    """Path channel: back-to-back ``varint(len) + PathPoint`` records.

    ``xy`` packs two 16-bit sign-magnitude values, each byte-swapped relative to the
    varint's natural order (see stream.proto comments); units are centimetres.
    """
    out: list[PathPoint] = []
    i = 0
    while i < len(body):
        try:
            length, j = read_varint(body, i)
        except ValueError:
            break
        rec = body[j : j + length]
        i = j + length
        if not rec or len(rec) != length or length > 16:
            break
        p = stream_pb2.PathPoint()
        try:
            p.ParseFromString(rec)
        except DecodeError:
            break
        v = p.xy
        x_raw = ((v & 0xFF) << 8) | ((v >> 8) & 0xFF)
        y_raw = (((v >> 16) & 0xFF) << 8) | ((v >> 24) & 0xFF)
        x = -(x_raw & 0x7FFF) if x_raw & 0x8000 else x_raw
        y = -(y_raw & 0x7FFF) if y_raw & 0x8000 else y_raw
        out.append(PathPoint(x=x, y=y, kind=PATH_KINDS.get(p.flags & 15, "unknown"), new_segment=bool((p.flags >> 4) & 1)))
    return out


_WIRE_VARINT, _WIRE_64, _WIRE_LEN, _WIRE_32 = 0, 1, 2, 5
_FD = FieldDescriptor
_SCALAR_WIRE = {
    _FD.TYPE_DOUBLE: _WIRE_64, _FD.TYPE_FIXED64: _WIRE_64, _FD.TYPE_SFIXED64: _WIRE_64,
    _FD.TYPE_FLOAT: _WIRE_32, _FD.TYPE_FIXED32: _WIRE_32, _FD.TYPE_SFIXED32: _WIRE_32,
    _FD.TYPE_STRING: _WIRE_LEN, _FD.TYPE_BYTES: _WIRE_LEN, _FD.TYPE_MESSAGE: _WIRE_LEN,
}


def _is_repeated(fd: Any) -> bool:
    rep = getattr(fd, "is_repeated", None)  # protobuf >= 6
    return bool(rep) if rep is not None else getattr(fd, "label", 0) == 3


def conforms(descriptor: Any, body: bytes, *, depth: int = 0) -> bool:
    """Walk the wire format and check every *known* field has the wire type its schema
    says, recursing into sub-messages and rejecting strings with control characters.

    Unknown field numbers are allowed (newer firmware adds fields). This is what tells a
    RestrictedZone from a DynamicData: both parse "successfully" as each other, but the
    nested Line bytes are not a valid Pose.
    """
    fields = {f.number: f for f in descriptor.fields}
    i, n = 0, len(body)
    while i < n:
        try:
            key, i = read_varint(body, i)
        except ValueError:
            return False
        number, wire = key >> 3, key & 7
        if number == 0:
            return False
        if wire == _WIRE_VARINT:
            try:
                _, i = read_varint(body, i)
            except ValueError:
                return False
            chunk = None
        elif wire == _WIRE_64:
            chunk, i = body[i : i + 8], i + 8
        elif wire == _WIRE_32:
            chunk, i = body[i : i + 4], i + 4
        elif wire == _WIRE_LEN:
            try:
                length, i = read_varint(body, i)
            except ValueError:
                return False
            chunk, i = body[i : i + length], i + length
            if len(chunk) != length:
                return False
        else:
            return False  # groups / invalid
        if i > n:
            return False
        fd = fields.get(number)
        if fd is None:
            continue
        expected = _SCALAR_WIRE.get(fd.type, _WIRE_VARINT)
        if wire != expected:
            # packed repeated scalars arrive length-delimited
            if not (wire == _WIRE_LEN and _is_repeated(fd) and expected != _WIRE_LEN):
                return False
            continue
        if fd.type == _FD.TYPE_MESSAGE and chunk is not None and depth < 8:
            if not conforms(fd.message_type, chunk, depth=depth + 1):
                return False
        elif fd.type == _FD.TYPE_STRING and chunk is not None:
            try:
                text = chunk.decode("utf-8")
            except UnicodeDecodeError:
                return False
            if any(ord(c) < 32 for c in text):
                return False
    return True


def _parse_exact(cls: Any, body: bytes) -> Any | None:
    """Parse ``body`` as ``cls`` only if its wire layout conforms to the schema."""
    if not conforms(cls.DESCRIPTOR, body):
        return None
    m = cls()
    m.ParseFromString(body)
    return m


def _decode_path_points_strict(body: bytes) -> tuple[list[PathPoint], int]:
    """Like :func:`decode_path_points` but also returns how many bytes were consumed and
    requires every record to be a schema-conformant PathPoint."""
    out: list[PathPoint] = []
    i = 0
    while i < len(body):
        try:
            length, j = read_varint(body, i)
        except ValueError:
            break
        rec = body[j : j + length]
        if not rec or len(rec) != length or length > 16 or not conforms(stream_pb2.PathPoint.DESCRIPTOR, rec):
            break
        pts = decode_path_points(body[i : j + length])
        if len(pts) != 1:
            break
        out.extend(pts)
        i = j + length
    return out, i


def _quad(q: Any) -> tuple[tuple[int, int], ...]:
    return tuple((pt.x, pt.y) for pt in (q.p0, q.p1, q.p2, q.p3))


class MapStream:
    """Accumulates map frames for one robot into a :class:`RobotMap`."""

    MAX_PATH_POINTS = 20000

    def __init__(self) -> None:
        self.map = RobotMap()
        self.channel_types: dict[int, str] = {}  # learned channel -> message name
        self._pending: dict[int, bytearray] = {}  # channel -> bytes of a chunked message
        self.frames_seen = 0
        self.frames_decoded = 0

    # ---- public

    def feed(self, payload: bytes, now: float | None = None) -> bool:
        """Consume one raw biz payload. Returns True if the map changed."""
        frame = parse_frame(payload)
        if frame is None:
            return False
        self.frames_seen += 1
        now = time.time() if now is None else now
        kind = self.channel_types.get(frame.channel)

        if kind == "path" or (kind is None and frame.partial and self._looks_like_path(frame.body)):
            return self._apply_path_frame(frame, now)

        if frame.partial:
            # chunk of a larger message; wait until a non-partial frame restarts the channel
            buf = self._pending.setdefault(frame.channel, bytearray())
            if frame.offset == len(buf):
                buf += frame.body
                return self._try_decode(frame.channel, bytes(buf), now, keep_pending=True)
            self._pending.pop(frame.channel, None)
            return False

        self._pending.pop(frame.channel, None)
        if frame.length > len(frame.body) + 8:  # first chunk of something bigger
            self._pending[frame.channel] = bytearray(frame.body)
        return self._try_decode(frame.channel, frame.body, now, keep_pending=False)

    def reset(self) -> None:
        self.map = RobotMap()
        self._pending.clear()

    # ---- decoding

    def _try_decode(self, channel: int, body: bytes, now: float, *, keep_pending: bool) -> bool:
        hint = self.channel_types.get(channel)
        order = [hint] if hint else []
        order += [k for k in ("map", "room_outline", "room_params", "path", "temporary_data", "dynamic_data", "obstacle_info", "restricted_zone", "map_description", "map_backup") if k != hint]
        for kind in order:
            handler = getattr(self, f"_apply_{kind}")
            try:
                changed = handler(body, now)
            except (DecodeError, ValueError, IndexError):
                continue
            if changed is None:  # parsed but not this message type
                continue
            self.channel_types[channel] = kind
            self.frames_decoded += 1
            if not keep_pending:
                self._pending.pop(channel, None)
            return changed
        return False

    @staticmethod
    def _looks_like_path(body: bytes) -> bool:
        pts = decode_path_points(body[:64])
        return len(pts) >= 2

    def _apply_map(self, body: bytes, now: float) -> bool | None:
        m = stream_pb2.Map()
        m.ParseFromString(body)
        if not m.info.width or not m.info.height or not m.pixels:
            return None
        pixels = _unpack_pixels(m)
        grid = Grid(m.info.width, m.info.height, m.info.resolution or 5, m.info.origin.x, m.info.origin.y)
        if len(pixels) < (grid.width * grid.height + 3) // 4:
            raise ValueError("map pixel buffer too small")
        docks = tuple((d.pose.x, d.pose.y, d.pose.theta) for d in m.info.docks_v2) or tuple((p.x, p.y, p.theta) for p in m.info.docks)
        full = m.frame == stream_pb2.Map.I
        if not full and self.map.grid == grid and self.map.pixels:
            # P-frame: cells with a known value overwrite, UNKNOWN keeps the old value
            old = bytearray(self.map.pixels)
            for i in range(grid.width * grid.height):
                v = (pixels[i >> 2] >> ((i & 3) * 2)) & 3
                if v:
                    shift = (i & 3) * 2
                    old[i >> 2] = (old[i >> 2] & ~(3 << shift)) | (v << shift)
            pixels = bytes(old)
        cur = self.map
        if cur.map_id and m.id and cur.map_id != m.id:
            cur = RobotMap()  # another map became active
        self.map = replace(cur, map_id=m.id or cur.map_id, releases=m.releases or cur.releases, frame_is_full=full, grid=grid, pixels=pixels, docks=docks or cur.docks, updated=now)
        return True

    def _apply_room_outline(self, body: bytes, now: float) -> bool | None:
        ro = stream_pb2.RoomOutline()
        ro.ParseFromString(body)
        if not ro.width or not ro.height or not ro.pixels:
            return None
        pixels = _unpack_pixels(ro)
        grid = Grid(ro.width, ro.height, ro.resolution or 5, ro.origin.x, ro.origin.y)
        if len(pixels) < grid.width * grid.height:
            raise ValueError("room outline buffer too small")
        self.map = replace(self.map, room_grid=grid, room_pixels=pixels, map_id=self.map.map_id or ro.map_id, updated=now)
        return True

    def _apply_room_params(self, body: bytes, now: float) -> bool | None:
        rp = _parse_exact(stream_pb2.RoomParams, body)
        if rp is None or not rp.rooms:
            return None
        rooms = {r.id: Room(id=r.id, name=r.name.strip(), scene_type=r.scene.type) for r in rp.rooms if r.id}
        if not rooms or any(any(ord(c) < 32 for c in r.name) for r in rooms.values()):
            return None
        self.map = replace(self.map, rooms=rooms, map_id=self.map.map_id or rp.map_id, updated=now)
        return True

    def _apply_restricted_zone(self, body: bytes, now: float) -> bool | None:
        rz = _parse_exact(stream_pb2.RestrictedZone, body)
        if rz is None or not rz.map_id:
            return None  # every real frame names its map
        walls = tuple(((w.p0.x, w.p0.y), (w.p1.x, w.p1.y)) for w in rz.virtual_walls)
        forbidden = tuple(_quad(q) for q in rz.forbidden_zones)
        no_mop = tuple(_quad(q) for q in rz.ban_mop_zones)
        self.map = replace(self.map, virtual_walls=walls, forbidden_zones=forbidden, no_mop_zones=no_mop, updated=now)
        return True

    def _apply_dynamic_data(self, body: bytes, now: float) -> bool | None:
        dd = _parse_exact(stream_pb2.DynamicData, body)
        if dd is None or not dd.HasField("cur_pose") or len(body) > 64:
            return None
        pose = (dd.cur_pose.x, dd.cur_pose.y, dd.cur_pose.theta)
        if pose == self.map.pose:
            return False
        self.map = replace(self.map, pose=pose, updated=now)
        return True

    def _apply_temporary_data(self, body: bytes, now: float) -> bool | None:
        td = _parse_exact(stream_pb2.TemporaryData, body)
        if td is None or not (td.HasField("select_rooms_clean") or td.HasField("select_zones_clean") or td.HasField("goto_location")):
            return None
        return False  # recognised, nothing to show yet

    def _apply_obstacle_info(self, body: bytes, now: float) -> bool | None:
        oi = _parse_exact(stream_pb2.ObstacleInfo, body)
        if oi is None or (not oi.map_id and not oi.obstacles):
            return None
        obstacles = tuple((o.object_type, o.show_points[0].x, o.show_points[0].y) for o in oi.obstacles if o.show_points)
        if obstacles == self.map.obstacles:
            return False
        self.map = replace(self.map, obstacles=obstacles, updated=now)
        return True

    def _apply_map_description(self, body: bytes, now: float) -> bool | None:
        md = _parse_exact(stream_pb2.MapDescription, body)
        if md is None or not md.map_id or not md.name or not md.name.isprintable():
            return None
        return False

    def _apply_map_backup(self, body: bytes, now: float) -> bool | None:
        mb = stream_pb2.MapBackup()
        mb.ParseFromString(body)
        if not mb.HasField("map") or not mb.map.info.width:
            return None
        changed = bool(self._apply_map(mb.map.SerializeToString(), now))
        if mb.HasField("rooms") and mb.rooms.width:
            changed |= bool(self._apply_room_outline(mb.rooms.SerializeToString(), now))
        if mb.room_params.rooms:
            changed |= bool(self._apply_room_params(mb.room_params.SerializeToString(), now))
        if mb.HasField("restricted_zone"):
            changed |= bool(self._apply_restricted_zone(mb.restricted_zone.SerializeToString(), now))
        return changed

    def _apply_path_frame(self, frame: Frame, now: float) -> bool:
        pts = decode_path_points(frame.body)
        if not pts:
            return False
        self.channel_types[frame.channel] = "path"
        self.frames_decoded += 1
        path = pts if (frame.offset == 0 or frame.clear) else self.map.path + tuple(pts)
        path = tuple(path)[-self.MAX_PATH_POINTS :]
        self.map = replace(self.map, path=path, updated=now)
        return True

    def _apply_path(self, body: bytes, now: float) -> bool | None:
        """Path channel seen as a whole (non-chunked) frame."""
        pts, consumed = _decode_path_points_strict(body)
        if len(pts) < 2 or consumed != len(body):
            return None
        self.map = replace(self.map, path=tuple(pts)[-self.MAX_PATH_POINTS :], updated=now)
        return True
