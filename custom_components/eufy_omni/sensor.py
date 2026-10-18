"""Sensors."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfArea, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import EufyOmniConfigEntry
from .client import CONSUMABLES, VacuumSnapshot
from .entity import EufyOmniEntity


@dataclass(frozen=True, kw_only=True)
class EufyOmniSensorDescription(SensorEntityDescription):
    value_fn: Callable[[VacuumSnapshot], object]


def _consumable(name: str) -> EufyOmniSensorDescription:
    return EufyOmniSensorDescription(
        key=f"consumable_{name}",
        translation_key=f"consumable_{name}",
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=name in ("side_brush", "rolling_brush", "filter_mesh", "mop", "dustbag"),
        value_fn=lambda s, n=name: s.consumable_hours.get(n),
    )


SENSORS: tuple[EufyOmniSensorDescription, ...] = (
    EufyOmniSensorDescription(
        key="battery",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda s: s.battery,
    ),
    EufyOmniSensorDescription(
        key="state",
        translation_key="state",
        device_class=SensorDeviceClass.ENUM,
        options=["idle", "cleaning", "paused", "returning", "docked", "error", "mapping", "remote_control", "unknown"],
        value_fn=lambda s: s.activity.value,
    ),
    EufyOmniSensorDescription(
        key="dock_activity",
        translation_key="dock_activity",
        device_class=SensorDeviceClass.ENUM,
        options=["idle", "washing", "drying", "collecting_dust", "adding_water", "recycling_water"],
        value_fn=lambda s: s.dock_activity.value,
    ),
    EufyOmniSensorDescription(
        key="clean_water",
        translation_key="clean_water",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda s: s.dock_clean_water,
    ),
    EufyOmniSensorDescription(
        key="error_code",
        translation_key="error_code",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda s: s.error_codes[0] if s.error_codes else 0,
    ),
    EufyOmniSensorDescription(
        key="last_clean_area",
        translation_key="last_clean_area",
        native_unit_of_measurement=UnitOfArea.SQUARE_METERS,
        device_class=SensorDeviceClass.AREA,
        value_fn=lambda s: s.last_clean_area,
    ),
    EufyOmniSensorDescription(
        key="last_clean_duration",
        translation_key="last_clean_duration",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        suggested_unit_of_measurement=UnitOfTime.MINUTES,
        value_fn=lambda s: s.last_clean_duration,
    ),
    EufyOmniSensorDescription(
        key="total_clean_count",
        translation_key="total_clean_count",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda s: s.total_clean_count,
    ),
    EufyOmniSensorDescription(
        key="total_clean_area",
        translation_key="total_clean_area",
        native_unit_of_measurement=UnitOfArea.SQUARE_METERS,
        device_class=SensorDeviceClass.AREA,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda s: s.total_clean_area,
    ),
    EufyOmniSensorDescription(
        key="total_clean_duration",
        translation_key="total_clean_duration",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        suggested_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda s: s.total_clean_duration,
    ),
    EufyOmniSensorDescription(
        key="wifi_signal",
        translation_key="wifi_signal",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda s: s.wifi_signal,
    ),
    EufyOmniSensorDescription(
        key="last_update",
        translation_key="last_update",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda s: datetime.fromtimestamp(s.last_update, UTC) if s.last_update else None,
    ),
    *(_consumable(n) for n in CONSUMABLES),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: EufyOmniConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(
        EufyOmniSensor(robot, desc) for robot in entry.runtime_data.robots.values() for desc in SENSORS
    )


class EufyOmniSensor(EufyOmniEntity, SensorEntity):
    entity_description: EufyOmniSensorDescription

    def __init__(self, robot, description: EufyOmniSensorDescription) -> None:  # noqa: ANN001
        super().__init__(robot)
        self.entity_description = description
        self._attr_unique_id = f"{robot.sn}_{description.key}"

    @property
    def native_value(self):  # noqa: ANN201
        return self.entity_description.value_fn(self.snapshot)
