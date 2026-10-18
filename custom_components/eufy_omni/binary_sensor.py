"""Binary sensors."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import EufyOmniConfigEntry
from .client import VacuumSnapshot
from .entity import EufyOmniEntity


@dataclass(frozen=True, kw_only=True)
class EufyOmniBinaryDescription(BinarySensorEntityDescription):
    value_fn: Callable[[VacuumSnapshot], bool | None]


BINARY_SENSORS: tuple[EufyOmniBinaryDescription, ...] = (
    EufyOmniBinaryDescription(
        key="charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        value_fn=lambda s: s.charging,
    ),
    EufyOmniBinaryDescription(key="docked", translation_key="docked", value_fn=lambda s: s.docked),
    EufyOmniBinaryDescription(
        key="problem",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda s: s.has_error,
    ),
    EufyOmniBinaryDescription(
        key="dock_connected",
        translation_key="dock_connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda s: s.dock_connected,
    ),
    EufyOmniBinaryDescription(
        key="online",
        translation_key="online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda s: s.online,
    ),
    EufyOmniBinaryDescription(
        key="push_connected",
        translation_key="push_connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda s: s.push_connected,
    ),
    EufyOmniBinaryDescription(
        key="do_not_disturb",
        translation_key="do_not_disturb",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda s: s.dnd_enabled,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: EufyOmniConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(
        EufyOmniBinarySensor(robot, d) for robot in entry.runtime_data.robots.values() for d in BINARY_SENSORS
    )


class EufyOmniBinarySensor(EufyOmniEntity, BinarySensorEntity):
    entity_description: EufyOmniBinaryDescription

    def __init__(self, robot, description: EufyOmniBinaryDescription) -> None:  # noqa: ANN001
        super().__init__(robot)
        self.entity_description = description
        self._attr_unique_id = f"{robot.sn}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        return self.entity_description.value_fn(self.snapshot)

    @property
    def available(self) -> bool:
        if self.entity_description.key in ("online", "push_connected"):
            return True
        return super().available
