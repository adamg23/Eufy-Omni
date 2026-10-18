"""Probe 3: exercise the high-level EufyAccount API end to end.

Usage: python tools/probe_account.py [seconds] [--model T211A] [--find] [--dock] [--volume]
Connects (cached session), prints every robot's decoded snapshot, optionally sends one
benign command to the chosen robot and prints push updates as they arrive.
"""

from __future__ import annotations

import asyncio
import dataclasses
import json
import os
import pathlib
import sys
import time

import aiohttp

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from eufy_omni_cloud import commands  # noqa: E402
from eufy_omni_cloud.account import EufyAccount, RobotVacuum  # noqa: E402
from tools._session import _load, _save, cache_path  # noqa: E402


def show(robot: RobotVacuum) -> None:
    s = dataclasses.asdict(robot.snapshot)
    s.pop("raw_dps", None)
    s["scenes"] = [f"{sc['id']}:{sc['name']}{'' if sc['valid'] else ' (invalid)'}" for sc in s["scenes"]]
    print(f"  {robot.model} …{robot.sn[-4:]} fw {robot.firmware}:")
    print("   ", json.dumps({k: v for k, v in s.items() if v not in (None, (), {}, [])}, default=str)[:900])


async def main() -> int:
    seconds = next((int(a) for a in sys.argv[1:] if a.isdigit()), 30)
    want = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "T211A"
    cached = _load() or {}
    async with aiohttp.ClientSession() as http:
        acct = EufyAccount(
            os.environ.get("EUFY_USERNAME", ""),
            os.environ.get("EUFY_PASSWORD", ""),
            http,
            openudid=cached.get("openudid"),
            saved_session=cached,
            poll_interval=3600,
        )
        await acct.async_connect()
        sess = acct.export_session()
        if sess and sess.get("access_token") != cached.get("access_token"):
            _save(acct._http.session, acct.openudid)  # noqa: SLF001
            print("session refreshed ->", cache_path())
        print(f"push_connected={acct.push_connected}; robots: {list(acct.robots.values())}")
        for r in acct.robots.values():
            show(r)
            r.add_listener(lambda rb: print(f"[{time.strftime('%H:%M:%S')}] update {rb.model}: activity={rb.snapshot.activity} battery={rb.snapshot.battery} charging={rb.snapshot.charging} find={rb.snapshot.find_robot} dock={rb.snapshot.dock_activity} paused={rb.snapshot.cleaning_paused}"))
        target = next((r for r in acct.robots.values() if r.model == want), None)
        if target is not None:
            if "--find" in sys.argv:
                await target.async_locate()
                print("sent: locate")
            if "--dock" in sys.argv:
                await target.async_return_to_dock()
                print("sent: return to dock (robot is on the dock, expect a no-op or ack)")
            if "--volume" in sys.argv:
                await target.async_set_volume(target.snapshot.volume or 80)
                print("sent: volume (unchanged)")
        print(f"listening {seconds}s …")
        await asyncio.sleep(seconds)
        await acct.async_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
