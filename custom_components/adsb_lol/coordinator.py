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
    ATTR_LONGITUDE,
    CONF_EXTRACT_TYPE
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
            update_interval=timedelta(minutes=entry.options.get("refresh_interval", DEFAULT_REFRESH_INTERVAL)),
        )
        self.config_entry = entry
        self.hass = hass
        
        self._data: dict[str, str] = {}

    async def _async_update_data(self) -> dict[str, str]:
        """Get the latest data from GTFS and GTFS relatime, depending refresh interval"""
        data = self.config_entry.data
        _LOGGER.debug("Self data: %s", data) 
        options = self.config_entry.options
        
        if data[CONF_EXTRACT_TYPE] in ["registration","callsign"]:
            self._url = str(data["url"]) + "/" + str(data["extract_type"]) + "/" + str(data["extract_param"])
            
        if data[CONF_EXTRACT_TYPE] == "point":
            device_tracker = self.hass.states.get(data["device_tracker_id"])
            latitude = device_tracker.attributes.get("latitude", None)
            longitude = device_tracker.attributes.get("longitude", None)
            _LOGGER.debug("Point search on lat: %s, lon: %s", latitude, longitude)
            self._url = str(data["url"]) + "/" + str(data["extract_type"]) + "/" + str(latitude) + "/" + str(longitude) + "/" + str(int(data["radius"] * 1000 / 1852) )
            _LOGGER.debug("Point search on URL: %s", self._url)

        self._flight = await self.hass.async_add_executor_job(
                    get_flight, self
                )     
                
        _LOGGER.debug("Coordinator data: %s", self._flight)
        
        if data[CONF_EXTRACT_TYPE] in ["registration","callsign"]:
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
        elif data[CONF_EXTRACT_TYPE] == "point":
            self._data = self._flight["ac"]
            
        return self._data

