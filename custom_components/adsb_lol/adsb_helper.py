"""The ADSB integration helper."""

import requests
import logging

_LOGGER = logging.getLogger(__name__)

def get_flight(self):
    response = requests.get(self._url)
    _LOGGER.debug ("Get flight: %s", response.json())
    return response.json()