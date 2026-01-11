"""Binary sensor platform for Daikin Humidifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import DaikinEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import DaikinDataUpdateCoordinator
    from .data import DaikinConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="filter_sign",
        name="Filter",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: DaikinConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        DaikinBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class DaikinBinarySensor(DaikinEntity, BinarySensorEntity):
    """Daikin binary_sensor class."""

    def __init__(
        self,
        coordinator: DaikinDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        status = self.coordinator.data.get("status", {})
        value = status.get(self.entity_description.key)
        # Assuming "1" means filter needs replacement
        return value == "1"
