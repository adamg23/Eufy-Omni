"""Endpoints and identifiers for the Eufy Clean cloud.

Documented in docs/PROTOCOL.md. The two OAuth-style client credential pairs are the
public ones baked into the EufyHome / Eufy Clean Android apps.
"""

from __future__ import annotations

HOME_API = "https://home-api.eufylife.com"
USER_API = "https://api.eufylife.com"
AIOT_API = "https://aiot-clean-api-pr.eufylife.com"

LOGIN_V2 = f"{HOME_API}/v1/user/v2/email/login"
LOGIN_V1 = f"{HOME_API}/v1/user/email/login"
USER_CENTER_INFO = f"{USER_API}/v1/user/user_center_info"
CLOUD_DEVICE_LIST = f"{USER_API}/v1/device/v2"
AIOT_DEVICE_LIST = f"{AIOT_API}/app/devicerelation/get_device_list"
AIOT_MQTT_INFO = f"{AIOT_API}/app/devicemanage/get_user_mqtt_info"

USER_AGENT = "EufyHome-Android-3.1.3-753"

# (label, url, client_id, client_secret, category) tried in order; v2 is the unified
# Eufy app and is the one that yields a user-center token for AIoT/MQTT devices.
LOGIN_CLIENTS: tuple[tuple[str, str, str, str, str], ...] = (
    ("v2", LOGIN_V2, "eufy-app", "8FHf22gaTKu7MZXqz5zytw", "Health"),
    ("v1", LOGIN_V1, "eufyhome-app", "GQCpr9dSp3uQpsOMgJ4xQ", "Home"),
)

MQTT_PORT = 8883
MQTT_KEEPALIVE_S = 60
TOPIC_CMD_REQ = "cmd/eufy_home/{model}/{sn}/req"
TOPIC_CMD_RES = "cmd/eufy_home/{model}/{sn}/res"
TOPIC_BIZ_RES = "biz/eufy_home/{model}/{sn}/res"


class Dp:
    """Tuya-style data point numbers carrying base64 protobuf values."""

    PLAY_PAUSE = "152"
    WORK_STATUS = "153"
    CLEAN_PARAM = "154"
    DIRECTION = "155"
    MULTI_MAP_SWITCH = "156"
    UNDISTURBED = "157"
    CLEAN_SPEED = "158"
    FIND_ROBOT = "160"
    VOLUME = "161"
    VOICE_LANGUAGE = "162"
    BATTERY = "163"
    MAP_EDIT = "164"
    MAP_DATA = "165"
    MAP_STREAM = "166"
    CLEAN_STATISTICS = "167"
    CONSUMABLES = "168"
    DEVICE_INFO = "169"
    MAP_EDIT_REQUEST = "170"
    MULTI_MAP_MANAGE = "172"
    STATION = "173"
    UNISETTING = "176"
    ERROR_CODE = "177"
    TELEMETRY = "179"
    SCENE = "180"
