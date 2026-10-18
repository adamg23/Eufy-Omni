"""Diagnostics with credentials, tokens and identifiers removed."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant

from . import EufyOmniConfigEntry
from .const import CONF_OPENUDID, CONF_SESSION

TO_REDACT = {CONF_PASSWORD, CONF_USERNAME, CONF_SESSION, CONF_OPENUDID, "user_id", "sn", "raw_dps"}
# Data points that embed identifiers (MAC/SSID/IP, Matter pairing code) never leave the snapshot's raw_dps.


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: EufyOmniConfigEntry) -> dict[str, Any]:
    account = entry.runtime_data
    robots = {}
    for robot in account.robots.values():
        snap = asdict(robot.snapshot)
        snap.pop("raw_dps", None)
        snap["raw_dp_keys"] = sorted(robot.snapshot.raw_dps)
        m = robot.map
        robots[f"…{robot.sn[-4:]}"] = {
            "model": robot.model,
            "firmware": robot.firmware,
            "snapshot": snap,
            "map": {
                "has_map": m.has_map,
                "map_id": m.map_id,
                "grid": asdict(m.grid) if m.grid else None,
                "rooms": {r.id: r.label for r in m.rooms.values()},
                "path_points": len(m.path),
                "channels": robot.map_stream.channel_types,
                "frames": [robot.map_stream.frames_decoded, robot.map_stream.frames_seen],
            },
        }
    return async_redact_data(
        {
            "entry": dict(entry.data),
            "push_connected": account.push_connected,
            "robots": robots,
        },
        TO_REDACT,
    )
