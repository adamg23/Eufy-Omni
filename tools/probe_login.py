"""Probe 1: login, account info, device lists, MQTT credential shape.

Reads EUFY_USERNAME / EUFY_PASSWORD from the environment. Prints a redacted summary and
writes sanitized fixtures to tests/fixtures/. Nothing secret is written to disk.
"""

from __future__ import annotations

import asyncio
import json
import os
import pathlib
import re
import sys

import aiohttp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.stdout.reconfigure(encoding="utf-8")

from tools._session import get_cloud  # noqa: E402

FIX = pathlib.Path(__file__).resolve().parents[1] / "tests" / "fixtures"
SECRET_KEYS = re.compile(
    r"(token|secret|key|pem|password|email|phone|sn$|device_sn|^id$|user_id|_id$|did|mac|ip$|ip_addr|wifi|ssid|address|name$|nick|openudid|thing_name|p2p|cover_path|license|prefix|server|time_zone)",
    re.I,
)


def sanitize(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if SECRET_KEYS.search(str(k)) and not isinstance(v, (dict, list)):
                out[k] = f"<{type(v).__name__}:{len(str(v))}>"
            else:
                out[k] = sanitize(v)
        return out
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    return obj


IDENTIFYING_DPS = {"166", "169"}  # Matter pairing code; MAC/SSID/IP/user id
SCENE_DP = "180"  # user-defined routine names


def scrub_scenes(value):
    """Rewrite dp 180 so routine names become generic; ids, validity, kinds and maps are kept."""
    from eufy_omni_cloud.codec import decode, encode
    from eufy_omni_cloud.pb import scene_pb2

    if not isinstance(value, str) or not value:
        return value
    try:
        msg = decode(scene_pb2.SceneResponse, value)
    except Exception:
        return "<dropped: undecodable scenes>"
    for info in msg.infos:
        info.name = f"Routine {info.id.value}"
    return encode(msg)


def scrub_dps(dps):
    out = {}
    for k, v in (dps or {}).items():
        if k in IDENTIFYING_DPS:
            out[k] = "<dropped: identifying>"
        elif k == SCENE_DP:
            out[k] = scrub_scenes(v)
        else:
            out[k] = v
    return out


def _dp_sort(k: str) -> int:
    return int(k) if k.isdigit() else 0


async def main() -> int:
    FIX.mkdir(parents=True, exist_ok=True)
    async with aiohttp.ClientSession() as http:
        cloud = await get_cloud(http)
        sess = cloud.session
        print("login:", sess)
        print("login response keys:", sorted(sess.raw_login))
        print("user-center keys:", sorted(sess.raw_user))

        cloud_devs = await cloud.async_cloud_devices()
        print(f"\ncloud device list (device/v2): {len(cloud_devs)}")
        for d in cloud_devs:
            prod = d.get("product") or {}
            print(
                "  -", d.get("alias_name") or d.get("name"),
                "| product_code", prod.get("product_code"), "| product name", prod.get("name"),
                "| model", d.get("device_model"), "| sw", d.get("software_version"),
                "| keys", sorted(d)[:25],
            )
        (FIX / "cloud_devices.json").write_text(json.dumps(sanitize(cloud_devs), indent=2), encoding="utf-8")

        aiot = await cloud.async_aiot_devices()
        print(f"\nAIoT device list: {len(aiot)}")
        for d in aiot:
            dps = d.get("dps") or {}
            print(
                "  -", d.get("alias_name") or d.get("device_name"), "| model", d.get("device_model"),
                "| sw", d.get("main_sw_version") or d.get("soft_version"),
                "| online", d.get("online", d.get("device_status")), "| keys", sorted(d),
            )
            print("    dps keys:", sorted(dps, key=_dp_sort))
            for k in sorted(dps, key=_dp_sort):
                v = dps[k]
                print(f"      {k}: {type(v).__name__} {str(v)[:70]}")
        for d in aiot:
            d["dps"] = scrub_dps(d.get("dps"))
        (FIX / "aiot_devices.json").write_text(json.dumps(sanitize(aiot), indent=2), encoding="utf-8")
        # dps values are protobuf state; 166/169 dropped and routine names (180) made generic
        snapshot = [{"device_model": d.get("device_model"), "dps": scrub_dps(d.get("dps"))} for d in aiot]
        (FIX / "aiot_dps_snapshot.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

        creds = await cloud.async_mqtt_credentials()
        print("\nMQTT credentials:", creds)
        print("  raw keys:", sorted(creds.raw))
        print(
            "  cert begins:", creds.certificate_pem[:27].replace("\n", " "),
            "| key begins:", creds.private_key[:27].replace("\n", " "),
        )
        (FIX / "mqtt_info_shape.json").write_text(json.dumps(sanitize(creds.raw), indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
