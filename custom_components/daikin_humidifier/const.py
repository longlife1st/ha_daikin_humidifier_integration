"""Constants for Daikin Humidifier."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "daikin_humidifier"

# API Endpoints
ENDPOINT_BASIC_INFO = "/common/basic_info"
ENDPOINT_MODEL_INFO = "/cleaner/get_model_info"
ENDPOINT_CONTROL_INFO = "/cleaner/get_control_info"
ENDPOINT_SET_CONTROL = "/cleaner/set_control_info"
ENDPOINT_SENSOR_INFO = "/cleaner/get_sensor_info"
ENDPOINT_UNIT_STATUS = "/cleaner/get_unit_status"

# Power states
POWER_OFF = "0"
POWER_ON = "1"

# Operating modes
MODE_AUTO = "1"  # おまかせ
MODE_ECO = "2"  # 節電
MODE_POLLEN = "3"  # 花粉
MODE_MOISTURIZE = "4"  # のど・はだ
MODE_CIRCULATOR = "5"  # サーキュレーター

MODES = {
    MODE_AUTO: "auto",
    MODE_ECO: "eco",
    MODE_POLLEN: "pollen",
    MODE_MOISTURIZE: "moisturize",
    MODE_CIRCULATOR: "circulator",
}

MODE_REVERSE = {v: k for k, v in MODES.items()}

# Humidity levels
HUMIDITY_OFF = "0"
HUMIDITY_LOW = "1"  # ひかえめ
HUMIDITY_NORMAL = "2"  # 標準
HUMIDITY_HIGH = "3"  # 高め

HUMIDITY_MODES = {
    HUMIDITY_OFF: "off",
    HUMIDITY_LOW: "low",
    HUMIDITY_NORMAL: "normal",
    HUMIDITY_HIGH: "high",
}

HUMIDITY_REVERSE = {v: k for k, v in HUMIDITY_MODES.items()}

# Fan speeds
FAN_AUTO = "0"  # 自動運転
FAN_SILENT = "1"  # しずか
FAN_LOW = "2"  # 弱
FAN_NORMAL = "3"  # 標準
FAN_TURBO = "5"  # ターボ

FAN_SPEEDS = {
    FAN_AUTO: "auto",
    FAN_SILENT: "silent",
    FAN_LOW: "low",
    FAN_NORMAL: "normal",
    FAN_TURBO: "turbo",
}

FAN_REVERSE = {v: k for k, v in FAN_SPEEDS.items()}
