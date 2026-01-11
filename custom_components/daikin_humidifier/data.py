"""Custom types for Daikin Humidifier."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import DaikinApiClient
    from .coordinator import DaikinDataUpdateCoordinator


type DaikinConfigEntry = ConfigEntry[DaikinData]


@dataclass
class DaikinData:
    """Data for the Daikin integration."""

    client: DaikinApiClient
    coordinator: DaikinDataUpdateCoordinator
    integration: Integration
