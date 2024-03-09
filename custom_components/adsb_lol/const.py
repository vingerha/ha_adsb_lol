"""Constants for the ADSB.lol integration."""
from homeassistant.const import STATE_UNKNOWN, Platform

DOMAIN = "adsb_lol"
PLATFORMS = [Platform.SENSOR]

# default values for options
CONF_REFRESH_INTERVAL = "refresh_interval"
ATTR_DEFAULT_REFRESH_INTERVAL = 5

CONF_RADIUS = "radius"
ATTR_DEFAULT_RADIUS = 40

CONF_ALTITUDE_LIMIT = "altitude_limit"
ATTR_DEFAULT_ALTITUDE_LIMIT = 0

DEFAULT_NAME = "ADSB.lol Sensor"
DEFAULT_PATH = "adsb_lol"
DEFAULT_PATH_GEOJSON = "www/adsb_lol"

CONF_REQUEST_TYPE = "request_type"

CONF_EXTRACT_TYPE = "extract_type"
CONF_URL = "url"
ATTR_DEFAULT_URL = "https://api.adsb.lol/v2"
CONF_EXTRACT_PARAM = "extract_param"



# constants used in helpers
ATTR_DELAY = "Delay"
ATTR_ICON = "Icon"
ATTR_UNIT_OF_MEASUREMENT = "unit_of_measurement"
ATTR_DEVICE_CLASS = "device_class"
ATTR_LATITUDE = "latitude"
ATTR_LONGITUDE = "longitude"


CONF_FILE = "file"
CONF_DEVICE_TRACKER_ID = "device_tracker_id"
CONF_NAME = "name"
CONF_REFRESH_INTERVAL = "refresh_interval"

CONF_ICON = "icon"
CONF_SERVICE_TYPE = "service_type"

DEFAULT_SERVICE = "Service"
DEFAULT_ICON = "mdi:plane"

TIME_STR_FORMAT = "%H:%M"


