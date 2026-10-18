"""Number entities."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import EufyOmniConfigEntry
from .entity import EufyOmniEntity

VOLUME = NumberEntityDescription(
    key="volume",
    translation_key="volume",
    native_min_value=0,
    native_max_value=100,
    native_step=10,
    native_unit_of_measurement=PERCENTAGE,
    mode=NumberMode.SLIDER,
    entity_category=EntityCategory.CONFIG,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: EufyOmniConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(EufyOmniVolume(robot) for robot in entry.runtime_data.robots.values())


class EufyOmniVolume(EufyOmniEntity, NumberEntity):
    entity_description = VOLUME

    def __init__(self, robot) -> None:  # noqa: ANN001
        super().__init__(robot)
        self._attr_unique_id = f"{robot.sn}_volume"

    @property
    def native_value(self) -> float | None:
        return self.snapshot.volume

    async def async_set_native_value(self, value: float) -> None:
        await self.robot.async_set_volume(int(value))
