"""Buttons."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import EufyOmniConfigEntry
from .entity import EufyOmniEntity

BUTTONS: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(key="locate", translation_key="locate"),
    ButtonEntityDescription(key="refresh", translation_key="refresh", entity_category=EntityCategory.DIAGNOSTIC),
    ButtonEntityDescription(key="wash_mop", translation_key="wash_mop"),
    ButtonEntityDescription(key="refresh_map", translation_key="refresh_map", entity_category=EntityCategory.DIAGNOSTIC),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: EufyOmniConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(
        EufyOmniButton(entry, robot, d) for robot in entry.runtime_data.robots.values() for d in BUTTONS
    )


class EufyOmniButton(EufyOmniEntity, ButtonEntity):
    def __init__(self, entry: EufyOmniConfigEntry, robot, description: ButtonEntityDescription) -> None:  # noqa: ANN001
        super().__init__(robot)
        self._entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{robot.sn}_{description.key}"

    async def async_press(self) -> None:
        key = self.entity_description.key
        if key == "locate":
            await self.robot.async_locate()
        elif key == "refresh":
            await self._entry.runtime_data.async_refresh()
        elif key == "wash_mop":
            await self.robot.async_wash_mop()
        elif key == "refresh_map":
            await self.robot.async_request_map(min_interval=0)
