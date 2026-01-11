"""Fan platform for Daikin Humidifier."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.util.percentage import (
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item,
)

from .const import (
    FAN_AUTO,
    FAN_REVERSE,
    FAN_SPEEDS,
    POWER_OFF,
    POWER_ON,
)
from .entity import DaikinEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import DaikinDataUpdateCoordinator
    from .data import DaikinConfigEntry

# Ordered list of fan speeds (excluding auto)
ORDERED_NAMED_FAN_SPEEDS = ["silent", "low", "normal", "turbo"]


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: DaikinConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the fan platform."""
    async_add_entities([DaikinFan(coordinator=entry.runtime_data.coordinator)])


class DaikinFan(DaikinEntity, FanEntity):
    """Daikin Fan entity for air circulation control."""

    _attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.PRESET_MODE
    _attr_name = "Fan"
    _attr_preset_modes: ClassVar[list[str]] = ["auto"]
    _attr_speed_count = len(ORDERED_NAMED_FAN_SPEEDS)

    def __init__(self, coordinator: DaikinDataUpdateCoordinator) -> None:
        """Initialize the fan."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_fan"

    @property
    def is_on(self) -> bool:
        """Return True if fan is on."""
        control = self.coordinator.data.get("control", {})
        return control.get("pow") == POWER_ON

    @property
    def percentage(self) -> int | None:
        """Return the current speed percentage."""
        control = self.coordinator.data.get("control", {})
        fan_value = control.get("airvol")

        # If in auto mode, return None (preset mode)
        if fan_value == FAN_AUTO:
            return None

        fan_mode = FAN_SPEEDS.get(fan_value)
        if fan_mode and fan_mode in ORDERED_NAMED_FAN_SPEEDS:
            return ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, fan_mode)
        return None

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode."""
        control = self.coordinator.data.get("control", {})
        fan_value = control.get("airvol")

        if fan_value == FAN_AUTO:
            return "auto"
        return None

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
    ) -> None:
        """Turn on the fan."""
        fan_speed = None

        if preset_mode == "auto":
            fan_speed = FAN_AUTO
        elif percentage is not None:
            fan_mode = percentage_to_ordered_list_item(
                ORDERED_NAMED_FAN_SPEEDS, percentage
            )
            fan_speed = FAN_REVERSE.get(fan_mode)

        if fan_speed:
            client = self.coordinator.config_entry.runtime_data.client
            await client.async_set_control_info(
                power=POWER_ON,
                fan_speed=fan_speed,
            )
        else:
            client = self.coordinator.config_entry.runtime_data.client
            await client.async_set_control_info(power=POWER_ON)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn off the fan."""
        await self.coordinator.config_entry.runtime_data.client.async_set_control_info(
            power=POWER_OFF
        )
        await self.coordinator.async_request_refresh()

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage."""
        fan_mode = percentage_to_ordered_list_item(
            ORDERED_NAMED_FAN_SPEEDS, percentage
        )
        fan_speed = FAN_REVERSE.get(fan_mode)

        if fan_speed:
            client = self.coordinator.config_entry.runtime_data.client
            await client.async_set_control_info(fan_speed=fan_speed)
            await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode."""
        if preset_mode == "auto":
            client = self.coordinator.config_entry.runtime_data.client
            await client.async_set_control_info(fan_speed=FAN_AUTO)
            await self.coordinator.async_request_refresh()
