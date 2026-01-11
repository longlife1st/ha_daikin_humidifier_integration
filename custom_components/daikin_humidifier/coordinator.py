"""DataUpdateCoordinator for Daikin Humidifier."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    DaikinApiClientAuthenticationError,
    DaikinApiClientError,
)

if TYPE_CHECKING:
    from .data import DaikinConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class DaikinDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: DaikinConfigEntry

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            client = self.config_entry.runtime_data.client

            # Fetch all needed data in parallel would be better, but for now sequential
            control_info = await client.async_get_control_info()
            sensor_info = await client.async_get_sensor_info()
            unit_status = await client.async_get_unit_status()

            return {
                "control": control_info,
                "sensors": sensor_info,
                "status": unit_status,
            }
        except DaikinApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except DaikinApiClientError as exception:
            raise UpdateFailed(exception) from exception
