"""Constants for the ADSB.lol integration."""
from homeassistant.const import STATE_UNKNOWN, Platform

DOMAIN = "adsb_lol"

# default values for options
CONF_REFRESH_INTERVAL = "refresh_interval"
DEFAULT_REFRESH_INTERVAL = 15
DEFAULT_TIMERANGE = 30

CONF_RADIUS = "radius"
ATTR_DEFAULT_RADIUS = 40

DEFAULT_NAME = "ADSB.lol Sensor"
DEFAULT_PATH = "adsb_lol"
DEFAULT_PATH_GEOJSON = "www/adsb_lol"

CONF_REQUEST_TYPE = "request_type"

CONF_EXTRACT_TYPE = "extract_type"
CONF_URL = "url"
DEFAULT_ATTR_URL = "https://api.adsb.lol/v2"
CONF_EXTRACT_PARAM = "extract_param"

CONF_DATA = "data"
CONF_DESTINATION = "destination"

PLATFORMS = [Platform.SENSOR]

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


