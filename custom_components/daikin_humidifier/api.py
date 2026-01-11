"""Daikin API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout

from .const import (
    ENDPOINT_BASIC_INFO,
    ENDPOINT_CONTROL_INFO,
    ENDPOINT_MODEL_INFO,
    ENDPOINT_SENSOR_INFO,
    ENDPOINT_SET_CONTROL,
    ENDPOINT_UNIT_STATUS,
)


class DaikinApiClientError(Exception):
    """Exception to indicate a general API error."""


class DaikinApiClientCommunicationError(DaikinApiClientError):
    """Exception to indicate a communication error."""


class DaikinApiClientAuthenticationError(DaikinApiClientError):
    """Exception to indicate an authentication error."""


def _parse_response(response_text: str) -> dict[str, str]:
    """Parse Daikin key=value format response.
    
    Example: "ret=OK,pow=1,mode=1,humd=2,airvol=3"
    Returns: {"ret": "OK", "pow": "1", "mode": "1", "humd": "2", "airvol": "3"}
    """
    result = {}
    for pair in response_text.split(","):
        if "=" in pair:
            key, value = pair.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise DaikinApiClientAuthenticationError(msg)
    response.raise_for_status()


class DaikinApiClient:
    """Daikin API Client for local HTTP communication."""

    def __init__(
        self,
        host: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize Daikin API Client.
        
        Args:
            host: IP address or hostname of the Daikin device
            session: aiohttp client session
        """
        self._host = host
        self._session = session
        self._base_url = f"http://{host}"

    async def async_get_basic_info(self) -> dict[str, str]:
        """Get basic device information."""
        return await self._api_wrapper(
            method="get",
            url=self._base_url + ENDPOINT_BASIC_INFO,
        )

    async def async_get_model_info(self) -> dict[str, str]:
        """Get model information."""
        return await self._api_wrapper(
            method="get",
            url=self._base_url + ENDPOINT_MODEL_INFO,
        )

    async def async_get_control_info(self) -> dict[str, str]:
        """Get current control settings (power, mode, humidity, fan)."""
        return await self._api_wrapper(
            method="get",
            url=self._base_url + ENDPOINT_CONTROL_INFO,
        )

    async def async_set_control_info(
        self,
        power: str | None = None,
        mode: str | None = None,
        humidity: str | None = None,
        fan_speed: str | None = None,
    ) -> dict[str, str]:
        """Set control parameters.
        
        Args:
            power: Power state ("0"=off, "1"=on)
            mode: Operating mode (1-5)
            humidity: Humidity level (0-3)
            fan_speed: Fan speed (0-5)
        """
        params = {}
        if power is not None:
            params["pow"] = power
        if mode is not None:
            params["mode"] = mode
        if humidity is not None:
            params["humd"] = humidity
        if fan_speed is not None:
            params["airvol"] = fan_speed

        return await self._api_wrapper(
            method="get",  # API accepts both GET and POST
            url=self._base_url + ENDPOINT_SET_CONTROL,
            params=params,
        )

    async def async_get_sensor_info(self) -> dict[str, str]:
        """Get sensor data (PM2.5, temperature, humidity)."""
        return await self._api_wrapper(
            method="get",
            url=self._base_url + ENDPOINT_SENSOR_INFO,
        )

    async def async_get_unit_status(self) -> dict[str, str]:
        """Get unit status (filter warnings, etc)."""
        return await self._api_wrapper(
            method="get",
            url=self._base_url + ENDPOINT_UNIT_STATUS,
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        params: dict | None = None,
    ) -> dict[str, str]:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    params=params,
                )
                _verify_response_or_raise(response)
                response_text = await response.text()
                return _parse_response(response_text)

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise DaikinApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise DaikinApiClientCommunicationError(msg) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise DaikinApiClientError(msg) from exception
