"""Base entity: one per robot, push-driven."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .client import RobotVacuum, VacuumSnapshot
from .const import DOMAIN, MODEL_NAMES


class EufyOmniEntity(Entity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, robot: RobotVacuum) -> None:
        self.robot = robot
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, robot.sn)},
            manufacturer="eufy",
            model=MODEL_NAMES.get(robot.model, robot.snapshot.product_name or robot.model),
            model_id=robot.model,
            name=robot.name,
            sw_version=robot.snapshot.firmware or robot.firmware,
        )

    @property
    def snapshot(self) -> VacuumSnapshot:
        return self.robot.snapshot

    @property
    def available(self) -> bool:
        return self.snapshot.online is not False

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.robot.add_listener(self._handle_update))

    def _handle_update(self, _robot: RobotVacuum) -> None:
        self.async_write_ha_state()
