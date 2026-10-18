"""Eufy Omni robot vacuums over the Eufy Clean cloud (MQTT push)."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .client import EufyAccount, EufyAuthError, EufyCloudError
from .const import CONF_OPENUDID, CONF_SESSION, PLATFORMS, POLL_INTERVAL_S

_LOGGER = logging.getLogger(__name__)

type EufyOmniConfigEntry = ConfigEntry[EufyAccount]


async def async_setup_entry(hass: HomeAssistant, entry: EufyOmniConfigEntry) -> bool:
    account = EufyAccount(
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        async_get_clientsession(hass),
        openudid=entry.data.get(CONF_OPENUDID),
        saved_session=entry.data.get(CONF_SESSION),
        poll_interval=POLL_INTERVAL_S,
    )
    try:
        await account.async_connect()
    except EufyAuthError as err:
        raise ConfigEntryAuthFailed(str(err)) from err
    except EufyCloudError as err:
        raise ConfigEntryNotReady(str(err)) from err
    if not account.robots:
        await account.async_close()
        raise ConfigEntryNotReady("No Eufy Clean robots on this account yet")

    exported = account.export_session()
    if exported and exported != entry.data.get(CONF_SESSION):
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, CONF_SESSION: exported, CONF_OPENUDID: account.openudid}
        )

    entry.runtime_data = account
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: EufyOmniConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        await entry.runtime_data.async_close()
    return ok
