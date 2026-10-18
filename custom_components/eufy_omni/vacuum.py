"""Vacuum entity."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components.vacuum import (
    StateVacuumEntity,
    VacuumActivity,
    VacuumEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import EufyOmniConfigEntry
from .client import FAN_SPEEDS, Activity
from .entity import EufyOmniEntity

ACTIVITY_MAP: dict[Activity, VacuumActivity] = {
    Activity.IDLE: VacuumActivity.IDLE,
    Activity.CLEANING: VacuumActivity.CLEANING,
    Activity.PAUSED: VacuumActivity.PAUSED,
    Activity.RETURNING: VacuumActivity.RETURNING,
    Activity.DOCKED: VacuumActivity.DOCKED,
    Activity.ERROR: VacuumActivity.ERROR,
    Activity.MAPPING: VacuumActivity.CLEANING,
    Activity.REMOTE_CONTROL: VacuumActivity.CLEANING,
}

SERVICE_START_SCENE = "start_scene"
SERVICE_START_ROOMS = "start_rooms"


async def async_setup_entry(
    hass: HomeAssistant, entry: EufyOmniConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(EufyOmniVacuum(robot) for robot in entry.runtime_data.robots.values())
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_START_SCENE,
        {vol.Exclusive("scene_id", "scene"): cv.positive_int, vol.Exclusive("scene_name", "scene"): cv.string},
        "async_start_scene_service",
    )
    platform.async_register_entity_service(
        SERVICE_START_ROOMS,
        {vol.Required("room_ids"): vol.All(cv.ensure_list, [cv.positive_int]), vol.Required("map_id"): cv.positive_int},
        "async_start_rooms_service",
    )


class EufyOmniVacuum(EufyOmniEntity, StateVacuumEntity):
    _attr_name = None
    _attr_supported_features = (
        VacuumEntityFeature.START
        | VacuumEntityFeature.PAUSE
        | VacuumEntityFeature.STOP
        | VacuumEntityFeature.RETURN_HOME
        | VacuumEntityFeature.FAN_SPEED
        | VacuumEntityFeature.LOCATE
        | VacuumEntityFeature.SEND_COMMAND
    )
    _attr_fan_speed_list = list(FAN_SPEEDS)
    _attr_translation_key = "robot"

    def __init__(self, robot) -> None:  # noqa: ANN001
        super().__init__(robot)
        self._attr_unique_id = robot.sn

    @property
    def activity(self) -> VacuumActivity | None:
        return ACTIVITY_MAP.get(self.snapshot.activity)

    @property
    def fan_speed(self) -> str | None:
        return self.snapshot.fan_speed

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        s = self.snapshot
        return {
            "eufy_state": s.work_state,
            "dock_activity": s.dock_activity.value,
            "clean_type": s.clean_type,
            "mop_level": s.mop_level,
            "clean_extent": s.clean_extent,
            "error_codes": list(s.error_codes),
            "warning_codes": list(s.warning_codes),
            "scenes": {sc.name: sc.id for sc in s.scenes if sc.valid},
            "push_connected": s.push_connected,
        }

    async def async_start(self) -> None:
        await self.robot.async_start()

    async def async_pause(self) -> None:
        await self.robot.async_pause()

    async def async_stop(self, **kwargs: Any) -> None:
        await self.robot.async_stop()

    async def async_return_to_base(self, **kwargs: Any) -> None:
        await self.robot.async_return_to_dock()

    async def async_locate(self, **kwargs: Any) -> None:
        await self.robot.async_locate()

    async def async_set_fan_speed(self, fan_speed: str, **kwargs: Any) -> None:
        await self.robot.async_set_fan_speed(fan_speed)

    async def async_send_command(self, command: str, params: dict[str, Any] | list[Any] | None = None, **kwargs: Any) -> None:
        """Raw data point write: command is the data point number, params {"value": ...}."""
        if not command.isdigit() or not isinstance(params, dict) or "value" not in params:
            raise ValueError("send_command expects command=<data point number> and params={'value': ...}")
        await self.robot.async_send({command: params["value"]})

    async def async_start_scene_service(self, scene_id: int | None = None, scene_name: str | None = None) -> None:
        if scene_id is None:
            match = next((sc for sc in self.snapshot.scenes if sc.name.lower() == (scene_name or "").lower()), None)
            if match is None:
                raise ValueError(f"Unknown scene {scene_name!r}")
            scene_id = match.id
        await self.robot.async_start_scene(scene_id)

    async def async_start_rooms_service(self, room_ids: list[int], map_id: int) -> None:
        await self.robot.async_start_rooms(room_ids, map_id)
