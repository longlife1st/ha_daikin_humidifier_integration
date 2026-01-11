"""Adds config flow for Daikin Humidifier."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    DaikinApiClient,
    DaikinApiClientAuthenticationError,
    DaikinApiClientCommunicationError,
    DaikinApiClientError,
)
from .const import DOMAIN, LOGGER


class DaikinFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Daikin Humidifier."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                info = await self._test_connection(
                    host=user_input[CONF_HOST],
                )
            except DaikinApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except DaikinApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except DaikinApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                # Use MAC address or device name as unique_id
                unique_id = info.get("mac", info.get("name", user_input[CONF_HOST]))
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                
                # Use device name as title if available, otherwise use host
                title = info.get("name", user_input[CONF_HOST])
                
                return self.async_create_entry(
                    title=title,
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_connection(self, host: str) -> dict[str, str]:
        """Validate the connection to the device."""
        client = DaikinApiClient(
            host=host,
            session=async_create_clientsession(self.hass),
        )
        return await client.async_get_basic_info()
