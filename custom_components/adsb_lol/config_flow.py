"""ConfigFlow for GTFS integration."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector

from .const import (
    DEFAULT_PATH, 
    DOMAIN, 
    CONF_NAME,
    DEFAULT_REFRESH_INTERVAL, 
    CONF_URL,
    CONF_EXTRACT_TYPE,
    CONF_EXTRACT_PARAM,
    DEFAULT_ATTR_URL
)    

from .adsb_helper import (
    get_flight,
)

_LOGGER = logging.getLogger(__name__)

@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GTFS."""

    VERSION = 1

    def __init__(self) -> None:
        """Init ConfigFlow."""
        self._pygtfs = ""
        self._data: dict[str, str] = {}
        self._user_inputs: dict = {}

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the source."""
        errors: dict[str, str] = {}
        
        return self.async_show_menu(
            step_id="user",
            menu_options=["flight_details"],
            description_placeholders={
                "model": "Example model",
            }
        )
                   
    async def async_step_flight_details(self, user_input: dict | None = None) -> FlowResult:
        """Handle the source."""
        errors: dict[str, str] = {}      
        if user_input is None:
            return self.async_show_form(
                step_id="flight_details",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_EXTRACT_TYPE): selector.SelectSelector(selector.SelectSelectorConfig(options=["registration", "callsign"], translation_key="extract_type")),
                        vol.Required(CONF_EXTRACT_PARAM): str,
                        vol.Required(CONF_URL, default=DEFAULT_ATTR_URL): str,
                        vol.Required(CONF_NAME): str,
                    },
                ),
            )

        self._user_inputs.update(user_input)
        _LOGGER.debug(f"UserInputs Start End: {self._user_inputs}")
        return self.async_create_entry(
                title=user_input[CONF_NAME], data=self._user_inputs
            )           
            


    async def _check_config(self, data):
        self._pygtfs = await self.hass.async_add_executor_job(
            get_gtfs, self.hass, DEFAULT_PATH, data, False
        )
        if self._pygtfs == "no_data_file":
            return "no_data_file"
        self._data = {
            "schedule": self._pygtfs,
            "origin": data["origin"],
            "destination": data["destination"],
            "offset": 0,
            "include_tomorrow": True,
            "gtfs_dir": DEFAULT_PATH,
            "name": data["name"],
            "next_departure": None,
            "file": data["file"],
            "route_type": data["route_type"]
        }
        # check and/or add indexes
        check_index = await self.hass.async_add_executor_job(
                    check_datasource_index, self.hass, self._pygtfs, DEFAULT_PATH, data["file"]
                )
        try:
            self._data["next_departure"] = await self.hass.async_add_executor_job(
                get_next_departure, self
            )
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.error(
                "Config: error getting gtfs data from generic helper: %s",
                {ex},
                exc_info=1,
            )
            return "generic_failure"
        if self._data["next_departure"]:
            return None
        return "stop_incorrect"