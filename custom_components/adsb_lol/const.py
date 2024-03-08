"""Constants for the ADSB.lol integration."""
from homeassistant.const import STATE_UNKNOWN, Platform

DOMAIN = "adsb_lol"

# default values for options
DEFAULT_REFRESH_INTERVAL = 15
DEFAULT_TIMERANGE = 30
DEFAULT_RADIUS = 400

DEFAULT_NAME = "ADSB.lol Sensor"
DEFAULT_PATH = "adsb_lol"
DEFAULT_PATH_GEOJSON = "www/adsb_lol"
DEFAULT_PATH_RT = "www/adsb_lol"

DEFAULT_ATTR_URL_REGISTRATION = "https://api.adsb.lol/v2/callsign"

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

CONF_URL_REGISTRATION = "url_registration"
CONF_FILE = "file"
CONF_DEVICE_TRACKER_ID = "device_tracker_id"
CONF_DIRECTION = "direction"
CONF_NAME = "name"
CONF_RADIUS = "radius"
CONF_REFRESH_INTERVAL = "refresh_interval"
CONF_REGISTRATION = "registration"

CONF_ICON = "icon"
CONF_SERVICE_TYPE = "service_type"

DEFAULT_SERVICE = "Service"
DEFAULT_ICON = "mdi:plane"

TIME_STR_FORMAT = "%H:%M"


