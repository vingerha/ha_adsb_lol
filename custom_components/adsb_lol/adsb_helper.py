"""The ADSB integration helper."""

import requests
import logging


_LOGGER = logging.getLogger(__name__)

def get_flight(self):
    _LOGGER.debug ("Get flight with data: %s", self)
    response = requests.get(self._url)
    _LOGGER.debug ("Get flight: %s", response.json())
    return response.json()
    
def get_point_of_interest(self):
    _LOGGER.debug ("Get poi with data: %s", self)
    response = requests.get(self._url)
    _LOGGER.debug ("Get flight rest output: %s", response.json())
    _response = []
    aircraft = {}
    for ac in response.json()["ac"]:
        _LOGGER.debug ("Get ac: %s", ac)
        if self._altitude_limit == 0 or (self._altitude_limit > 0 and ac["alt_geom"] * 1000 / 0.3048 < self._altitude_limit):
            aircraft["callsign"] = ac["flight"]
            aircraft["registration"] = ac["r"]
            aircraft["icao24"] = ac["hex"]
            aircraft["groundspeed"] = ac["gs"]
            aircraft["altitude_baro"] = ac["alt_baro"]
            aircraft["altitude_geom"] = ac["alt_geom"]
            aircraft["latitude"] = ac["lat"]
            aircraft["longitude"] = ac["lon"]
            _response.append(aircraft)
    
    _LOGGER.debug ("Get flight transformed: %s", _response)
    
    return _response    