"""Humidifier platform for Daikin Humidifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityFeature,
)

from .const import (
    HUMIDITY_HIGH,
    HUMIDITY_LOW,
    HUMIDITY_NORMAL,
    HUMIDITY_OFF,
    MODE_REVERSE,
    MODES,
    POWER_OFF,
    POWER_ON,
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
    """Set up the humidifier platform."""
    async_add_entities([DaikinHumidifier(coordinator=entry.runtime_data.coordinator)])


class DaikinHumidifier(DaikinEntity, HumidifierEntity):
    """Daikin Humidifier entity."""

    _attr_device_class = HumidifierDeviceClass.HUMIDIFIER
    _attr_supported_features = HumidifierEntityFeature.MODES
    _attr_name = None  # Use device name
    _attr_min_humidity = 0
    _attr_max_humidity = 100

    def __init__(self, coordinator: DaikinDataUpdateCoordinator) -> None:
        """Initialize the humidifier."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_humidifier"

    @property
    def is_on(self) -> bool:
        """Return True if device is on."""
        control = self.coordinator.data.get("control", {})
        return control.get("pow") == POWER_ON

    @property
    def mode(self) -> str | None:
        """Return the current mode (operating mode of the device)."""
        control = self.coordinator.data.get("control", {})
        mode_value = control.get("mode")
        return MODES.get(mode_value)

    @property
    def available_modes(self) -> list[str]:
        """Return available modes."""
        return list(MODE_REVERSE.keys())

    @property
    def target_humidity(self) -> int | None:
        """Return the target humidity."""
        control = self.coordinator.data.get("control", {})
        humd_value = control.get("humd")

        # Map Daikin levels to percentages
        humidity_map = {
            HUMIDITY_OFF: 0,
            HUMIDITY_LOW: 40,
            HUMIDITY_NORMAL: 50,
            HUMIDITY_HIGH: 60,
        }
        return humidity_map.get(humd_value, 50)

    @property
    def current_humidity(self) -> int | None:
        """Return the current humidity."""
        sensors = self.coordinator.data.get("sensors", {})
        humi = sensors.get("hhum")
        if humi:
            try:
                return int(humi)
            except (ValueError, TypeError):
                return None
        return None

    async def async_turn_on(self) -> None:
        """Turn the device on."""
        await self.coordinator.config_entry.runtime_data.client.async_set_control_info(
            power=POWER_ON
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn the device off."""
        await self.coordinator.config_entry.runtime_data.client.async_set_control_info(
            power=POWER_OFF
        )
        await self.coordinator.async_request_refresh()

    async def async_set_humidity(self, humidity: int) -> None:
        """Set new target humidity."""
        # Map percentage to Daikin levels
        # Low=40%, Normal=50%, High=60%
        if humidity == 0:
            humd_value = HUMIDITY_OFF
        elif humidity <= 45:  # noqa: PLR2004
            humd_value = HUMIDITY_LOW
        elif humidity <= 55:  # noqa: PLR2004
            humd_value = HUMIDITY_NORMAL
        else:
            humd_value = HUMIDITY_HIGH

        client = self.coordinator.config_entry.runtime_data.client
        await client.async_set_control_info(humidity=humd_value)
        await self.coordinator.async_request_refresh()

    async def async_set_mode(self, mode: str) -> None:
        """Set new operating mode."""
        mode_value = MODE_REVERSE.get(mode)
        if mode_value:
            client = self.coordinator.config_entry.runtime_data.client
            await client.async_set_control_info(mode=mode_value)
            await self.coordinator.async_request_refresh()
