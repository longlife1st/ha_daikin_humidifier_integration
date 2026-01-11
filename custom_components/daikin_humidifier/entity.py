"""DaikinEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DaikinDataUpdateCoordinator


class DaikinEntity(CoordinatorEntity[DaikinDataUpdateCoordinator]):
    """Base Daikin Entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: DaikinDataUpdateCoordinator) -> None:
        """Initialize Daikin Entity."""
        super().__init__(coordinator)

        # Get device info from config entry or coordinator data
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=coordinator.config_entry.title,
            manufacturer="Daikin",
        )
