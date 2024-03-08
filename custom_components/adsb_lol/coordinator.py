"""Data Update coordinator for the GTFS integration."""
from __future__ import annotations

import datetime
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import homeassistant.util.dt as dt_util

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
        
        self._pygtfs = ""
        self._data: dict[str, str] = {}

    async def _async_update_data(self) -> dict[str, str]:
        """Get the latest data from GTFS and GTFS relatime, depending refresh interval"""
        data = self.config_entry.data
        options = self.config_entry.options
        previous_data = None if self.data is None else self.data.copy()
        _LOGGER.debug("Previous data: %s", previous_data)  

        self._pygtfs = get_gtfs(
            self.hass, DEFAULT_PATH, data, False
        )        
        self._data = {
            "adsb_dir": DEFAULT_PATH,
            "name": data["name"],
        }           
        
        return self._data

