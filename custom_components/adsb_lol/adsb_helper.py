"""The ADSB integration helper."""

import requests
import logging


_LOGGER = logging.getLogger(__name__)

def get_flight(self):
    _LOGGER.debug ("Get flight with data: %s", self)
    response = requests.get(self._url)
    _LOGGER.debug ("Get flight rest output: %s", response.json())
    return response.json()
    
def get_point_of_interest(self):
    _LOGGER.debug ("Get flight poi with data: %s", self)
    response = requests.get(self._url)
    _LOGGER.debug ("Get flight poi rest output: %s", response.json())
    _response = []
    _response_h = []
    aircraft = {}
    aircraft_h = {}
    for ac in response.json()["ac"]:
        if self._altitude_limit == 0 or (self._altitude_limit > 0 and ac["alt_geom"] < self._altitude_limit * 1000 / 0.3048 ):
            aircraft["callsign"] = ac.get("flight", None)
            aircraft["registration"] = ac.get("r", None)
            self._reg = ac.get("r", "NoReg")
            aircraft["icao24"] = ac.get("hex", None)
            aircraft["type"] = ac.get("t", None)
            aircraft["groundspeed_nmph"] = ac.get("gs",None)
            aircraft["true_airspeed_nmph"] = ac.get("tas",None)
            aircraft["mach"] = ac.get("mach", None)
            aircraft["altitude_baro_ft"] = ac.get("alt_baro", None)
            aircraft["altitude_geom_ft"] = ac.get("alt_geom", None)
            aircraft["latitude"] = ac.get("lat", None)
            aircraft["longitude"] = ac.get("lon", None)
            aircraft_h[str(self._reg)] = aircraft.copy()

    _response_h = aircraft_h

    _LOGGER.debug ("Get flight poi: %s", response.json())
    return _response_h   