"""Probe 2: connect to the broker with the account certificate and listen.

Usage: python tools/probe_mqtt.py [seconds] [--model T211A] [--all]
Prints every status message's data points (decoded where a schema is known) and
summarises biz/ (map stream) traffic. Raw frames go to captures/ (git-ignored).
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import pathlib
import sys
import time

import aiohttp

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from google.protobuf.json_format import MessageToDict  # noqa: E402

from eufy_omni_cloud.codec import decode  # noqa: E402
from tools._session import get_cloud  # noqa: E402
from eufy_omni_cloud.mqtt import EufyMqtt  # noqa: E402
from eufy_omni_cloud.pb import (  # noqa: E402
    app_device_info_pb2,
    clean_param_pb2,
    clean_statistics_pb2,
    consumable_pb2,
    control_pb2,
    error_code_pb2,
    scene_pb2,
    station_pb2,
    undisturbed_pb2,
    unisetting_pb2,
    work_status_pb2,
)

SCHEMA = {
    "152": control_pb2.ModeCtrlResponse,
    "153": work_status_pb2.WorkStatus,
    "154": clean_param_pb2.CleanParamResponse,
    "157": undisturbed_pb2.UndisturbedResponse,
    "167": clean_statistics_pb2.CleanStatistics,
    "168": consumable_pb2.ConsumableResponse,
    "169": app_device_info_pb2.DeviceInfo,
    "173": station_pb2.StationResponse,
    "176": unisetting_pb2.UnisettingResponse,
    "177": error_code_pb2.ErrorCode,
    "180": scene_pb2.SceneResponse,
}
CAP = ROOT / "captures"


def describe(dp: str, value) -> str:
    if not isinstance(value, str) or value.isdigit() or dp not in SCHEMA:
        return repr(value)
    try:
        d = MessageToDict(decode(SCHEMA[dp], value), preserving_proto_field_name=True)
        if dp == "169":
            for k in ("device_mac", "wifi_name", "wifi_ip", "last_user_id", "sn"):
                d.pop(k, None)
        return json.dumps(d)[:400]
    except Exception as err:  # noqa: BLE001
        return f"<{type(err).__name__}> {value[:40]}"


async def main() -> int:
    seconds = next((int(a) for a in sys.argv[1:] if a.isdigit()), 60)
    want_model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "T211A"
    all_devices = "--all" in sys.argv
    CAP.mkdir(exist_ok=True)
    stats = {"cmd": 0, "biz": 0}
    log = (CAP / f"mqtt_{int(time.time())}.raw.json").open("w", encoding="utf-8")

    async with aiohttp.ClientSession() as http:
        cloud = await get_cloud(http)
        openudid = cloud.openudid
        devices = await cloud.async_aiot_devices()
        creds = await cloud.async_mqtt_credentials()
        print("broker:", creds.endpoint, "| devices:", [(d["device_model"], d.get("main_sw_version")) for d in devices])

        bus = EufyMqtt(creds, openudid)

        def on_dps(sn: str, dps: dict) -> None:
            stats["cmd"] += 1
            ts = time.strftime("%H:%M:%S")
            print(f"[{ts}] {sn[-4:]} status: {len(dps)} dp(s)")
            for k in sorted(dps, key=lambda x: int(x) if x.isdigit() else 0):
                print(f"      {k}: {describe(k, dps[k])}")

        def on_raw(topic: str, payload: bytes) -> None:
            kind = topic.split("/")[0]
            if kind == "biz":
                stats["biz"] += 1
                print(f"[{time.strftime('%H:%M:%S')}] biz frame {len(payload)} bytes: {payload[:120]!r}")
            log.write(json.dumps({"t": time.time(), "topic": topic.split("/")[0] + "/.../" + topic.split("/")[-1], "payload": base64.b64encode(payload).decode()}) + "\n")

        for d in devices:
            if all_devices or d["device_model"] == want_model:
                bus.add_device(d["device_model"], d["device_sn"], on_dps=on_dps, on_raw=on_raw)
                print("subscribed:", d["device_model"], "sn …" + d["device_sn"][-4:])
        await bus.async_start()
        try:
            await bus.async_wait_connected(20)
        except TimeoutError:
            print("no CONNACK within 20 s")
            await bus.async_stop()
            return 1
        await asyncio.sleep(2)
        print(f"connected; subscribe reason codes {bus.last_subscribe_codes}; listening {seconds}s …")
        target = next((d for d in devices if d["device_model"] == want_model), None)
        if target and "--find" in sys.argv:
            # Harmless: the robot says "I'm here". Expect an echo of dp 160 (and often 152/153).
            await bus.async_send_dps(target["device_model"], target["device_sn"], {"160": True})
            print("sent find-robot (160=true)")
        if target and "--volume" in sys.argv:
            vol = int(target["dps"].get("161", 80))
            await bus.async_send_dps(target["device_model"], target["device_sn"], {"161": vol})
            print(f"sent volume {vol} (unchanged value, expect echo)")
        await asyncio.sleep(seconds)
        await bus.async_stop()
    log.close()
    print("done:", stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
