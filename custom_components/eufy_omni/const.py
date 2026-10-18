"""Constants for the Eufy Omni integration."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "eufy_omni"

CONF_SESSION = "session"
CONF_OPENUDID = "openudid"

POLL_INTERVAL_S = 300

PLATFORMS: list[Platform] = [
    Platform.VACUUM,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.SELECT,
    Platform.NUMBER,
    Platform.CAMERA,
]

MODEL_NAMES: dict[str, str] = {
    "T211A": "Omni C28",
    "T2351": "X10 Pro Omni",
    "T2320": "X9 Pro",
    "T2280": "Omni C20",
    "T2292": "Omni E28",
}
