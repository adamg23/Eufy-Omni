"""Probe 4: capture and decode the biz/ map stream.

Usage: python tools/probe_map.py [seconds] [--model T211A] [--get-maps] [--get-one N]

Subscribes to the robot's biz/ topic, writes every frame raw to captures/ (git-ignored),
and tries to decode each frame against the stream schemas. ``--get-maps`` sends
MultiMapsManageRequest{MAP_GET_ALL} on dp 172 (a read), ``--get-one N`` MAP_GET_ONE for
cloud map id N, to see whether the robot answers with map data while idle.
"""

from __future__ import annotations

import asyncio
import base64
import json
import pathlib
import sys
import time

import aiohttp

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from google.protobuf.json_format import MessageToDict  # noqa: E402
from google.protobuf.message import Message  # noqa: E402

from eufy_omni_cloud.codec import decode, encode, read_varint  # noqa: E402
from eufy_omni_cloud.mqtt import EufyMqtt  # noqa: E402
from eufy_omni_cloud.pb import multi_maps_pb2, stream_pb2  # noqa: E402
from tools._session import get_cloud  # noqa: E402

CAP = ROOT / "captures"
CANDIDATES = [
    "Metadata", "MapInfo", "Map", "RoomOutline", "RoomParams", "RestrictedZone",
    "DynamicData", "TemporaryData", "ObstacleInfo", "CruiseData", "MapDescription",
    "MapBackup", "SceneWrap",
]


def _clean(m: Message) -> tuple[int, int]:
    """(fields set, problems) – problems = unknown fields or control chars in strings."""
    n = bad = 0
    for fd, val in m.ListFields():
        n += 1
        for v in val if fd.label == fd.LABEL_REPEATED else [val]:
            if isinstance(v, Message):
                a, b = _clean(v)
                n += a
                bad += b
            elif isinstance(v, str) and any(ord(c) < 32 for c in v):
                bad += 1
    return n, bad


def guess(raw: bytes) -> list[tuple[str, int, str]]:
    out = []
    for name in CANDIDATES:
        cls = getattr(stream_pb2, name)
        try:
            m = cls()
            m.ParseFromString(raw)
        except Exception:  # noqa: BLE001
            continue
        n, bad = _clean(m)
        if m.SerializeToString() != raw:
            bad += 1  # not a byte-exact round trip: probably the wrong message type
        if n and not bad:
            d = MessageToDict(m, preserving_proto_field_name=True)
            for k in ("pixels",):
                if k in d:
                    d[k] = f"<{len(m.pixels)} bytes>"
            if "map" in d and isinstance(d["map"], dict) and "pixels" in d["map"]:
                d["map"]["pixels"] = f"<{len(m.map.pixels)} bytes>"
            if "rooms" in d and isinstance(d["rooms"], dict) and "pixels" in d["rooms"]:
                d["rooms"]["pixels"] = f"<{len(m.rooms.pixels)} bytes>"
            out.append((name, n, json.dumps(d)[:700]))
    return sorted(out, key=lambda t: -t[1])


def parse_biz(payload: bytes) -> dict | None:
    try:
        env = json.loads(payload)
        p = env.get("payload")
        if isinstance(p, str):
            p = json.loads(p)
        return {"head": env.get("head"), "payload": p}
    except Exception:  # noqa: BLE001
        return None


async def main() -> int:
    seconds = next((int(a) for a in sys.argv[1:] if a.isdigit()), 90)
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "T211A"
    CAP.mkdir(exist_ok=True)
    log = (CAP / f"map_{int(time.time())}.raw.jsonl").open("w", encoding="utf-8")
    stats = {"cmd": 0, "biz": 0, "biz_bytes": 0}

    async with aiohttp.ClientSession() as http:
        cloud = await get_cloud(http)
        devices = await cloud.async_aiot_devices()
        creds = await cloud.async_mqtt_credentials()
        target = next(d for d in devices if d["device_model"] == model)
        bus = EufyMqtt(creds, cloud.openudid, tap_requests=True)

        def on_dps(sn: str, dps: dict) -> None:
            stats["cmd"] += 1
            keys = sorted(dps, key=lambda x: int(x) if x.isdigit() else 0)
            print(f"[{time.strftime('%H:%M:%S')}] status dps {keys}")
            if "172" in dps:
                try:
                    r = decode(multi_maps_pb2.MultiMapsManageResponse, dps["172"])
                    print("      172:", json.dumps(MessageToDict(r, preserving_proto_field_name=True))[:600])
                except Exception as err:  # noqa: BLE001
                    print("      172 undecodable:", err)

        def on_raw(topic: str, payload: bytes) -> None:
            kind = topic.split("/")[0]
            log.write(json.dumps({"t": time.time(), "topic": kind + "/" + topic.rsplit("/", 1)[-1], "payload": base64.b64encode(payload).decode()}) + "\n")
            log.flush()
            ts = time.strftime("%H:%M:%S")
            direction = topic.rsplit("/", 1)[-1]
            if direction == "req":
                # another client (the app) talking to the robot
                env = parse_biz(payload)
                p = (env or {}).get("payload") or {}
                if kind == "cmd" and isinstance(p, dict) and isinstance(p.get("data"), dict):
                    for k, v in p["data"].items():
                        shown = v if not isinstance(v, str) or len(v) < 80 else v[:80] + "…"
                        print(f"[{ts}] APP→robot cmd dp {k} = {shown!r}")
                else:
                    print(f"[{ts}] APP→robot {kind} {len(payload)} B: {payload[:200]!r}")
                return
            stats["biz"] += 1
            stats["biz_bytes"] += len(payload)
            env = parse_biz(payload)
            if env is None:
                print(f"[{ts}] biz {len(payload)} B, not JSON: {payload[:80]!r}")
                return
            p = env["payload"] or {}
            data = p.get("data")
            keys = {k: (v if k != "data" else "…") for k, v in p.items()} if isinstance(p, dict) else p
            print(f"[{ts}] biz {len(payload)} B payload keys={keys}")
            if isinstance(data, dict):
                inner = {k: v for k, v in data.items() if k != "data"}
                hexdata = data.get("data", "")
                print(f"      data fields={inner} hex_len={len(hexdata)}")
                try:
                    raw = bytes.fromhex(hexdata)
                except ValueError:
                    print("      data is not hex; first 60:", hexdata[:60])
                    return
                try:
                    length, pos = read_varint(raw, 0)
                except ValueError:
                    length, pos = -1, 0
                body = raw[pos:] if length == len(raw) - pos else raw
                print(f"      varint prefix {length} (payload {len(raw) - pos}) -> body {len(body)} B")
                for name, n, s in guess(body)[:3]:
                    print(f"      ≈ {name} ({n} fields): {s}")

        bus.add_device(model, target["device_sn"], on_dps=on_dps, on_raw=on_raw)
        await bus.async_start()
        await bus.async_wait_connected(20)
        await asyncio.sleep(2)
        print(f"connected; subscribe codes {bus.last_subscribe_codes}; listening {seconds}s")

        if "--get-maps" in sys.argv:
            req = multi_maps_pb2.MultiMapsManageRequest(method=multi_maps_pb2.MultiMapsManageRequest.MAP_GET_ALL, seq=int(time.time()) % 1000)
            await bus.async_send_dps(model, target["device_sn"], {"172": encode(req)})
            print("sent 172 = MultiMapsManageRequest{MAP_GET_ALL}")
        if "--get-one" in sys.argv:
            mid = int(sys.argv[sys.argv.index("--get-one") + 1])
            req = multi_maps_pb2.MultiMapsManageRequest(method=multi_maps_pb2.MultiMapsManageRequest.MAP_GET_ONE, seq=int(time.time()) % 1000)
            req.common.cloud_mapid = mid
            await bus.async_send_dps(model, target["device_sn"], {"172": encode(req)})
            print(f"sent 172 = MultiMapsManageRequest{{MAP_GET_ONE {mid}}}")

        if "--wake" in sys.argv:
            # What the phone app does when its map screen opens (captured 2026-10-17):
            # 169 = AppInfo (who is asking), then 153 = KeepAliveRequest with a microsecond
            # timestamp, repeated with force_sync=true. The robot then streams every map channel.
            from eufy_omni_cloud.pb import app_device_info_pb2, keepalive_pb2

            app = app_device_info_pb2.AppInfo(platform=app_device_info_pb2.AppInfo.PF_ANDROID, app_version="6.1.11", user_id=creds.user_id, data_center=app_device_info_pb2.AppInfo.AZ)
            app.app_function.multi_maps.version = 1
            app.app_function.multi_maps.options = 1
            app.app_function.optimization.version = 1
            app.app_function.optimization.options = 14
            await bus.async_send_dps(model, target["device_sn"], {"169": encode(app)})
            print(f"[{time.strftime('%H:%M:%S')}] sent 169 = AppInfo")
            await asyncio.sleep(1.5)
            ka = keepalive_pb2.KeepAliveRequest(timestamp=int(time.time() * 1_000_000))
            before = stats["biz"]
            await bus.async_send_dps(model, target["device_sn"], {"153": encode(ka)})
            print(f"[{time.strftime('%H:%M:%S')}] sent 153 = KeepAliveRequest (no force)")
            await asyncio.sleep(8)
            print(f"      biz frames since: {stats['biz'] - before}")
            if stats["biz"] == before:
                ka = keepalive_pb2.KeepAliveRequest(timestamp=int(time.time() * 1_000_000), force_sync=True)
                await bus.async_send_dps(model, target["device_sn"], {"153": encode(ka)})
                print(f"[{time.strftime('%H:%M:%S')}] sent 153 = KeepAliveRequest(force_sync=True)")
                await asyncio.sleep(8)
                print(f"      biz frames since: {stats['biz'] - before}")

        if "--keepalive" in sys.argv:
            # Try KeepAliveRequest on each listed dp, 15 s apart, watching for any reaction.
            from eufy_omni_cloud.pb import keepalive_pb2

            dps_to_try = sys.argv[sys.argv.index("--keepalive") + 1].split(",")
            for dp in dps_to_try:
                req = keepalive_pb2.KeepAliveRequest(timestamp=int(time.time() * 1000), force_sync="--force" in sys.argv)
                before = (stats["cmd"], stats["biz"])
                await bus.async_send_dps(model, target["device_sn"], {dp: encode(req)})
                print(f"[{time.strftime('%H:%M:%S')}] sent {dp} = KeepAliveRequest(force_sync={'--force' in sys.argv})")
                await asyncio.sleep(15)
                print(f"      reaction: status +{stats['cmd'] - before[0]}, biz +{stats['biz'] - before[1]}")

        await asyncio.sleep(seconds)
        await bus.async_stop()
    log.close()
    print("done:", stats, "| raw log:", log.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
