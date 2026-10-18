"""Select entities for cleaning parameters."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import EufyOmniConfigEntry
from .client import CLEAN_EXTENTS, CLEAN_TYPES, MOP_LEVELS, RobotVacuum, VacuumSnapshot
from .entity import EufyOmniEntity


@dataclass(frozen=True, kw_only=True)
class EufyOmniSelectDescription(SelectEntityDescription):
    value_fn: Callable[[VacuumSnapshot], str | None]
    set_fn: Callable[[RobotVacuum, str], Awaitable[None]]


SELECTS: tuple[EufyOmniSelectDescription, ...] = (
    EufyOmniSelectDescription(
        key="clean_type",
        translation_key="clean_type",
        options=list(CLEAN_TYPES),
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda s: s.clean_type,
        set_fn=lambda r, v: r.async_set_clean_type(v),
    ),
    EufyOmniSelectDescription(
        key="mop_level",
        translation_key="mop_level",
        options=list(MOP_LEVELS),
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda s: s.mop_level,
        set_fn=lambda r, v: r.async_set_mop_level(v),
    ),
    EufyOmniSelectDescription(
        key="clean_extent",
        translation_key="clean_extent",
        options=list(CLEAN_EXTENTS),
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda s: s.clean_extent,
        set_fn=lambda r, v: r.async_set_clean_extent(v),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: EufyOmniConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(EufyOmniSelect(robot, d) for robot in entry.runtime_data.robots.values() for d in SELECTS)


class EufyOmniSelect(EufyOmniEntity, SelectEntity):
    entity_description: EufyOmniSelectDescription

    def __init__(self, robot: RobotVacuum, description: EufyOmniSelectDescription) -> None:
        super().__init__(robot)
        self.entity_description = description
        self._attr_unique_id = f"{robot.sn}_{description.key}"

    @property
    def current_option(self) -> str | None:
        return self.entity_description.value_fn(self.snapshot)

    async def async_select_option(self, option: str) -> None:
        await self.entity_description.set_fn(self.robot, option)
