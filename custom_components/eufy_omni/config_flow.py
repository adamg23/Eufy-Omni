"""Config flow: one entry per Eufy account."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .client import EufyAccount, EufyAuthError, EufyCloudError
from .const import CONF_OPENUDID, CONF_SESSION, DOMAIN

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): TextSelector(TextSelectorConfig(type=TextSelectorType.EMAIL)),
        vol.Required(CONF_PASSWORD): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD)),
    }
)


class EufyOmniConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._reauth_entry = None

    async def _try_login(self, username: str, password: str) -> tuple[dict[str, Any] | None, str | None]:
        account = EufyAccount(username, password, async_get_clientsession(self.hass))
        try:
            await account.async_login()
            robots = await account.async_discover()
        except EufyAuthError:
            return None, "invalid_auth"
        except EufyCloudError:
            return None, "cannot_connect"
        except Exception:  # noqa: BLE001
            _LOGGER.exception("Unexpected error during Eufy login")
            return None, "unknown"
        if not robots:
            return None, "no_robot"
        return {
            CONF_USERNAME: username,
            CONF_PASSWORD: password,
            CONF_OPENUDID: account.openudid,
            CONF_SESSION: account.export_session(),
            "user_id": account.export_session().get("user_id"),
        }, None

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            data, error = await self._try_login(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            if data is not None:
                await self.async_set_unique_id(data["user_id"] or user_input[CONF_USERNAME].lower())
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=user_input[CONF_USERNAME], data=data)
            errors["base"] = error or "unknown"
        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA, errors=errors)

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> ConfigFlowResult:
        self._reauth_entry = self._get_reauth_entry()
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        entry = self._reauth_entry
        assert entry is not None
        if user_input is not None:
            data, error = await self._try_login(entry.data[CONF_USERNAME], user_input[CONF_PASSWORD])
            if data is not None:
                return self.async_update_reload_and_abort(entry, data={**entry.data, **data})
            errors["base"] = error or "unknown"
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_PASSWORD): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD))}),
            description_placeholders={"username": entry.data[CONF_USERNAME]},
            errors=errors,
        )
