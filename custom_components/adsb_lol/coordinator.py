"""Data Update coordinator for the GTFS integration."""
from __future__ import annotations

import datetime
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import homeassistant.util.dt as dt_util

from .adsb_helper import (
    get_flight,
)

from .const import (
    DEFAULT_PATH, 
    DEFAULT_REFRESH_INTERVAL, 
    ATTR_LATITUDE,
    ATTR_LONGITUDE
)    

_LOGGER = logging.getLogger(__name__)


class ADSBUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for the GTFS integration."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=entry.entry_id,
            update_interval=timedelta(minutes=1),
        )
        self.config_entry = entry
        self.hass = hass
        
        self._data: dict[str, str] = {}

    async def _async_update_data(self) -> dict[str, str]:
        """Get the latest data from GTFS and GTFS relatime, depending refresh interval"""
        data = self.config_entry.data
        _LOGGER.debug("Self data: %s", data) 
        options = self.config_entry.options
        previous_data = None if self.data is None else self.data.copy()
        _LOGGER.debug("Previous data: %s", previous_data)  
        
        self._url = str(data["url"]) + "/" + str(data["extract_type"]) + "/" + str(data["extract_param"])

        self._flight = await self.hass.async_add_executor_job(
                    get_flight, self
                )     
                
        _LOGGER.debug("Coordinator data: %s", self._flight)
        
        self._data = {
            "registration": self._flight["ac"][0]["r"],
            "callsign": self._flight["ac"][0]["flight"],
            "type": self._flight["ac"][0]["t"],
            "icao24": self._flight["ac"][0]["hex"],
            "altitude_baro": self._flight["ac"][0]["alt_baro"],
            "altitude_geom": self._flight["ac"][0]["alt_geom"],
            "ground_speed": self._flight["ac"][0]["gs"],
            "mach": self._flight["ac"][0]["mach"],
            "latitude": self._flight["ac"][0]["lat"],
            "longitude": self._flight["ac"][0]["lon"],
        }           
        
        return self._data

