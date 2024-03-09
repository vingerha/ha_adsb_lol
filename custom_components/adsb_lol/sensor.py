"""Support for ADSB.lol"""
from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify
import homeassistant.util.dt as dt_util

from .const import (
    ATTR_LATITUDE,
    DOMAIN,
)

from .coordinator import ADSBUpdateCoordinator, ADSBPointUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    ) -> None:
    """Initialize the setup."""  
    sensors = []    
    if config_entry.data.get('device_tracker_id',None):
        coordinator: ADSBPointUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
           "coordinator"
        ]
        await coordinator.async_config_entry_first_refresh()
        _LOGGER.debug("Incoming data: %s:", coordinator.data)
        sensors.append(
                ADSBPointSensor(coordinator, config_entry.data.get('device_tracker_id') )
            )

    else:
        coordinator: ADSBUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
           "coordinator"
        ]
        await coordinator.async_config_entry_first_refresh()
        
        sensors.append(
                ADSBFlightTrackerSensor(coordinator)
            )
    
    async_add_entities(sensors, False)
    
class ADSBFlightTrackerSensor(CoordinatorEntity, SensorEntity):
    """Implementation of a ADSB Flight tracker via registration departures sensor."""

    def __init__(self, coordinator) -> None:
        """Initialize the ADSB sensor."""
        super().__init__(coordinator)
        self._name = self.coordinator.data['registration']
        self._attributes: dict[str, Any] = {}

        self._attr_unique_id = f"adsb-{self._name}_{self.coordinator.data['registration']}"
        self._attr_device_info = DeviceInfo(
            name=f"ADSB - {self._name}",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"ADSB - {self._name}")},
            manufacturer="ADSB",
            model=self._name,
        )
        self._attributes = self._update_attrs()
        self._attr_extra_state_attributes = self._attributes

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name + "_flight_tracker"
        
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_attrs()
        super()._handle_coordinator_update()

    def _update_attrs(self):  # noqa: C901 PLR0911
        _LOGGER.debug("SENSOR: %s, update with attr data: %s", self._name, self.coordinator.data)
        self._state: str | None = None
        self._state = self.coordinator.data["callsign"]
        self._attr_native_value = self._state 

         
        self._attr_extra_state_attributes = self.coordinator.data
        return self._attr_extra_state_attributes
        
class ADSBPointSensor(CoordinatorEntity, SensorEntity):
    """Implementation of a ADBS flights around poi sensor."""

    def __init__(self, coordinator, device_tracker_id) -> None:
        """Initialize the ADSB sensor."""
        super().__init__(coordinator)             
        self._name = device_tracker_id
        self._device_tracker_id = device_tracker_id
        self._attributes: dict[str, Any] = {}

        self._attr_unique_id = f"adsb-in-radius-{self._name}"
        self._attr_device_info = DeviceInfo(
            name=f"ADSB - {self._name}",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"ADSB - {self._name}")},
            manufacturer="ADSB",
            model=self._name,
        )
        self._attributes = self._update_attrs()
        self._attr_extra_state_attributes = self._attributes

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "flights_in_radius_" + self._name

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_attrs()
        super()._handle_coordinator_update()

    def _update_attrs(self):  # noqa: C901 PLR0911
        _LOGGER.debug("SENSOR: %s, update with attr data: %s", self._name, self.coordinator.data)
        self._state: str | None = None
        # if no data or extracting, aircraft
        #state
        self._attr_native_value = len(self.coordinator.data)
        
        
        self._attributes["aircraft"] = self.coordinator.data
        self._attr_extra_state_attributes = self._attributes

        return self._attr_extra_state_attributes        
