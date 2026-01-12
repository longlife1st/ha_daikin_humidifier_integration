"""Select platform for Daikin Humidifier."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from homeassistant.components.select import SelectEntity

from .const import (
    HUMIDITY_MODES,
    HUMIDITY_REVERSE,
)
from .entity import DaikinEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import DaikinDataUpdateCoordinator
    from .data import DaikinConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: DaikinConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    async_add_entities(
        [DaikinHumidityModeSelect(coordinator=entry.runtime_data.coordinator)]
    )


class DaikinHumidityModeSelect(DaikinEntity, SelectEntity):
    """Daikin humidity mode select entity."""

    _attr_translation_key = "humidity_mode"
    _attr_options: ClassVar[list[str]] = list(HUMIDITY_MODES.values())

    def __init__(self, coordinator: DaikinDataUpdateCoordinator) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_humidity_mode"

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        control = self.coordinator.data.get("control", {})
        humd_value = control.get("humd")
        return HUMIDITY_MODES.get(humd_value)

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        humd_value = HUMIDITY_REVERSE.get(option)
        if humd_value:
            client = self.coordinator.config_entry.runtime_data.client
            await client.async_set_control_info(humidity=humd_value)
            await self.coordinator.async_request_refresh()
