from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BtAppMsg(_message.Message):
    __slots__ = ("get_product_info", "get_ap_list", "distribute", "req")
    class GetProductInfo(_message.Message):
        __slots__ = ("get", "distribute_version", "remedy_field", "country")
        class RemedyField(_message.Message):
            __slots__ = ("distribute_version2",)
            DISTRIBUTE_VERSION2_FIELD_NUMBER: _ClassVar[int]
            distribute_version2: int
            def __init__(self, distribute_version2: _Optional[int] = ...) -> None: ...
        class Country(_message.Message):
            __slots__ = ("code",)
            CODE_FIELD_NUMBER: _ClassVar[int]
            code: str
            def __init__(self, code: _Optional[str] = ...) -> None: ...
        GET_FIELD_NUMBER: _ClassVar[int]
        DISTRIBUTE_VERSION_FIELD_NUMBER: _ClassVar[int]
        REMEDY_FIELD_FIELD_NUMBER: _ClassVar[int]
        COUNTRY_FIELD_NUMBER: _ClassVar[int]
        get: bool
        distribute_version: int
        remedy_field: BtAppMsg.GetProductInfo.RemedyField
        country: BtAppMsg.GetProductInfo.Country
        def __init__(self, get: _Optional[bool] = ..., distribute_version: _Optional[int] = ..., remedy_field: _Optional[_Union[BtAppMsg.GetProductInfo.RemedyField, _Mapping]] = ..., country: _Optional[_Union[BtAppMsg.GetProductInfo.Country, _Mapping]] = ...) -> None: ...
    class GetApList(_message.Message):
        __slots__ = ("max_num",)
        MAX_NUM_FIELD_NUMBER: _ClassVar[int]
        max_num: int
        def __init__(self, max_num: _Optional[int] = ...) -> None: ...
    class Distribute(_message.Message):
        __slots__ = ("ssid", "passwd", "token", "user_id", "time_zone_id", "domain", "app_id", "house_id", "dev_name", "hub_name")
        SSID_FIELD_NUMBER: _ClassVar[int]
        PASSWD_FIELD_NUMBER: _ClassVar[int]
        TOKEN_FIELD_NUMBER: _ClassVar[int]
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_ZONE_ID_FIELD_NUMBER: _ClassVar[int]
        DOMAIN_FIELD_NUMBER: _ClassVar[int]
        APP_ID_FIELD_NUMBER: _ClassVar[int]
        HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
        DEV_NAME_FIELD_NUMBER: _ClassVar[int]
        HUB_NAME_FIELD_NUMBER: _ClassVar[int]
        ssid: str
        passwd: str
        token: str
        user_id: str
        time_zone_id: str
        domain: str
        app_id: str
        house_id: str
        dev_name: str
        hub_name: str
        def __init__(self, ssid: _Optional[str] = ..., passwd: _Optional[str] = ..., token: _Optional[str] = ..., user_id: _Optional[str] = ..., time_zone_id: _Optional[str] = ..., domain: _Optional[str] = ..., app_id: _Optional[str] = ..., house_id: _Optional[str] = ..., dev_name: _Optional[str] = ..., hub_name: _Optional[str] = ...) -> None: ...
    class Debug(_message.Message):
        __slots__ = ("d_data",)
        D_DATA_FIELD_NUMBER: _ClassVar[int]
        d_data: str
        def __init__(self, d_data: _Optional[str] = ...) -> None: ...
    GET_PRODUCT_INFO_FIELD_NUMBER: _ClassVar[int]
    GET_AP_LIST_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    REQ_FIELD_NUMBER: _ClassVar[int]
    get_product_info: BtAppMsg.GetProductInfo
    get_ap_list: BtAppMsg.GetApList
    distribute: BtAppMsg.Distribute
    req: BtAppMsg.Debug
    def __init__(self, get_product_info: _Optional[_Union[BtAppMsg.GetProductInfo, _Mapping]] = ..., get_ap_list: _Optional[_Union[BtAppMsg.GetApList, _Mapping]] = ..., distribute: _Optional[_Union[BtAppMsg.Distribute, _Mapping]] = ..., req: _Optional[_Union[BtAppMsg.Debug, _Mapping]] = ...) -> None: ...

class BtRobotMsg(_message.Message):
    __slots__ = ("product_info", "ap_list", "distribute_result", "ack")
    class ProductInfo(_message.Message):
        __slots__ = ("ret", "brand", "code_name", "model", "name", "alisa_name", "cloud_pid", "mac", "distribute_version", "remedy_field")
        class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            E_OK: _ClassVar[BtRobotMsg.ProductInfo.Result]
            E_FAIL: _ClassVar[BtRobotMsg.ProductInfo.Result]
        E_OK: BtRobotMsg.ProductInfo.Result
        E_FAIL: BtRobotMsg.ProductInfo.Result
        class RemedyField(_message.Message):
            __slots__ = ("distribute_version2",)
            DISTRIBUTE_VERSION2_FIELD_NUMBER: _ClassVar[int]
            distribute_version2: int
            def __init__(self, distribute_version2: _Optional[int] = ...) -> None: ...
        RET_FIELD_NUMBER: _ClassVar[int]
        BRAND_FIELD_NUMBER: _ClassVar[int]
        CODE_NAME_FIELD_NUMBER: _ClassVar[int]
        MODEL_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        ALISA_NAME_FIELD_NUMBER: _ClassVar[int]
        CLOUD_PID_FIELD_NUMBER: _ClassVar[int]
        MAC_FIELD_NUMBER: _ClassVar[int]
        DISTRIBUTE_VERSION_FIELD_NUMBER: _ClassVar[int]
        REMEDY_FIELD_FIELD_NUMBER: _ClassVar[int]
        ret: BtRobotMsg.ProductInfo.Result
        brand: str
        code_name: str
        model: str
        name: str
        alisa_name: str
        cloud_pid: str
        mac: str
        distribute_version: int
        remedy_field: BtRobotMsg.ProductInfo.RemedyField
        def __init__(self, ret: _Optional[_Union[BtRobotMsg.ProductInfo.Result, str]] = ..., brand: _Optional[str] = ..., code_name: _Optional[str] = ..., model: _Optional[str] = ..., name: _Optional[str] = ..., alisa_name: _Optional[str] = ..., cloud_pid: _Optional[str] = ..., mac: _Optional[str] = ..., distribute_version: _Optional[int] = ..., remedy_field: _Optional[_Union[BtRobotMsg.ProductInfo.RemedyField, _Mapping]] = ...) -> None: ...
    class ApList(_message.Message):
        __slots__ = ("ap_info",)
        class ApInfo(_message.Message):
            __slots__ = ("ssid", "dbm")
            SSID_FIELD_NUMBER: _ClassVar[int]
            DBM_FIELD_NUMBER: _ClassVar[int]
            ssid: str
            dbm: int
            def __init__(self, ssid: _Optional[str] = ..., dbm: _Optional[int] = ...) -> None: ...
        AP_INFO_FIELD_NUMBER: _ClassVar[int]
        ap_info: _containers.RepeatedCompositeFieldContainer[BtRobotMsg.ApList.ApInfo]
        def __init__(self, ap_info: _Optional[_Iterable[_Union[BtRobotMsg.ApList.ApInfo, _Mapping]]] = ...) -> None: ...
    class DistributeResult(_message.Message):
        __slots__ = ("value", "mac", "pid", "uuid", "authkey", "dbm", "aiot_result")
        class Value(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            E_OK: _ClassVar[BtRobotMsg.DistributeResult.Value]
            E_SRV_ERR: _ClassVar[BtRobotMsg.DistributeResult.Value]
            E_AP_NOT_FOUND: _ClassVar[BtRobotMsg.DistributeResult.Value]
            E_PASSWD_ERR: _ClassVar[BtRobotMsg.DistributeResult.Value]
            E_DHCP_ERR: _ClassVar[BtRobotMsg.DistributeResult.Value]
            E_GW_ERR: _ClassVar[BtRobotMsg.DistributeResult.Value]
            E_DNS_ERR: _ClassVar[BtRobotMsg.DistributeResult.Value]
            E_NET_ERR: _ClassVar[BtRobotMsg.DistributeResult.Value]
        E_OK: BtRobotMsg.DistributeResult.Value
        E_SRV_ERR: BtRobotMsg.DistributeResult.Value
        E_AP_NOT_FOUND: BtRobotMsg.DistributeResult.Value
        E_PASSWD_ERR: BtRobotMsg.DistributeResult.Value
        E_DHCP_ERR: BtRobotMsg.DistributeResult.Value
        E_GW_ERR: BtRobotMsg.DistributeResult.Value
        E_DNS_ERR: BtRobotMsg.DistributeResult.Value
        E_NET_ERR: BtRobotMsg.DistributeResult.Value
        class AiotResult(_message.Message):
            __slots__ = ("get_mqtt_info_ret", "get_data_point_ret", "connect_mqtt_ret", "bind_ret")
            GET_MQTT_INFO_RET_FIELD_NUMBER: _ClassVar[int]
            GET_DATA_POINT_RET_FIELD_NUMBER: _ClassVar[int]
            CONNECT_MQTT_RET_FIELD_NUMBER: _ClassVar[int]
            BIND_RET_FIELD_NUMBER: _ClassVar[int]
            get_mqtt_info_ret: int
            get_data_point_ret: int
            connect_mqtt_ret: int
            bind_ret: int
            def __init__(self, get_mqtt_info_ret: _Optional[int] = ..., get_data_point_ret: _Optional[int] = ..., connect_mqtt_ret: _Optional[int] = ..., bind_ret: _Optional[int] = ...) -> None: ...
        VALUE_FIELD_NUMBER: _ClassVar[int]
        MAC_FIELD_NUMBER: _ClassVar[int]
        PID_FIELD_NUMBER: _ClassVar[int]
        UUID_FIELD_NUMBER: _ClassVar[int]
        AUTHKEY_FIELD_NUMBER: _ClassVar[int]
        DBM_FIELD_NUMBER: _ClassVar[int]
        AIOT_RESULT_FIELD_NUMBER: _ClassVar[int]
        value: BtRobotMsg.DistributeResult.Value
        mac: str
        pid: str
        uuid: str
        authkey: str
        dbm: int
        aiot_result: BtRobotMsg.DistributeResult.AiotResult
        def __init__(self, value: _Optional[_Union[BtRobotMsg.DistributeResult.Value, str]] = ..., mac: _Optional[str] = ..., pid: _Optional[str] = ..., uuid: _Optional[str] = ..., authkey: _Optional[str] = ..., dbm: _Optional[int] = ..., aiot_result: _Optional[_Union[BtRobotMsg.DistributeResult.AiotResult, _Mapping]] = ...) -> None: ...
    class Debug(_message.Message):
        __slots__ = ("d_data",)
        D_DATA_FIELD_NUMBER: _ClassVar[int]
        d_data: str
        def __init__(self, d_data: _Optional[str] = ...) -> None: ...
    PRODUCT_INFO_FIELD_NUMBER: _ClassVar[int]
    AP_LIST_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTE_RESULT_FIELD_NUMBER: _ClassVar[int]
    ACK_FIELD_NUMBER: _ClassVar[int]
    product_info: BtRobotMsg.ProductInfo
    ap_list: BtRobotMsg.ApList
    distribute_result: BtRobotMsg.DistributeResult
    ack: BtRobotMsg.Debug
    def __init__(self, product_info: _Optional[_Union[BtRobotMsg.ProductInfo, _Mapping]] = ..., ap_list: _Optional[_Union[BtRobotMsg.ApList, _Mapping]] = ..., distribute_result: _Optional[_Union[BtRobotMsg.DistributeResult, _Mapping]] = ..., ack: _Optional[_Union[BtRobotMsg.Debug, _Mapping]] = ...) -> None: ...
