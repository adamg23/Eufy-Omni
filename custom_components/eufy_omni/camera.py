"""Map camera: renders the robot's live map as a PNG."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import EufyOmniConfigEntry
from .client import RobotVacuum, render_png
from .entity import EufyOmniEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: EufyOmniConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    async_add_entities(EufyOmniMapCamera(robot) for robot in entry.runtime_data.robots.values())


class EufyOmniMapCamera(EufyOmniEntity, Camera):
    _attr_translation_key = "map"
    _attr_supported_features = CameraEntityFeature(0)
    _attr_frame_interval = 2.0

    def __init__(self, robot: RobotVacuum) -> None:
        EufyOmniEntity.__init__(self, robot)
        Camera.__init__(self)
        self.content_type = "image/png"
        self._attr_unique_id = f"{robot.sn}_map"
        self._png: bytes | None = None
        self._png_for: float = -1.0

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self.async_on_remove(self.robot.add_map_listener(self._handle_map))

    def _handle_map(self, _robot: RobotVacuum) -> None:
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        return super().available and self.robot.map.has_map

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        m = self.robot.map
        attrs: dict[str, Any] = {"map_id": m.map_id, "rooms": {r.id: r.label for r in m.rooms.values()}}
        if m.grid is not None:
            attrs.update(
                width_cells=m.grid.width,
                height_cells=m.grid.height,
                cell_cm=m.grid.resolution,
                origin_cm=[m.grid.origin_x, m.grid.origin_y],
            )
        if m.pose is not None:
            attrs["robot_position_cm"] = [m.pose[0], m.pose[1]]
        if m.docks:
            attrs["dock_position_cm"] = [m.docks[0][0], m.docks[0][1]]
        attrs["path_points"] = len(m.path)
        attrs["map_updated"] = m.updated or None
        return attrs

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        m = self.robot.map
        if not m.has_map:
            return None
        if self._png is None or self._png_for != m.updated:
            size = max(width or 0, height or 0) or 800
            try:
                self._png = await self.hass.async_add_executor_job(lambda: render_png(m, max_size=min(size, 1600)))
            except Exception:  # noqa: BLE001
                _LOGGER.exception("map render failed")
                return self._png
            self._png_for = m.updated
        return self._png
