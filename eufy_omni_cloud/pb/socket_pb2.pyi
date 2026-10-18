from . import ble_pb2 as _ble_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SocketBroadcast(_message.Message):
    __slots__ = ("is_bind", "device_sn", "user_id")
    IS_BIND_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SN_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    is_bind: bool
    device_sn: str
    user_id: str
    def __init__(self, is_bind: _Optional[bool] = ..., device_sn: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class SocketVerify(_message.Message):
    __slots__ = ("random", "device_sn", "user_id")
    RANDOM_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SN_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    random: str
    device_sn: str
    user_id: str
    def __init__(self, random: _Optional[str] = ..., device_sn: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class SocketTransData(_message.Message):
    __slots__ = ("type", "distribute")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        E_DISTRIBUTE: _ClassVar[SocketTransData.Type]
        E_DP: _ClassVar[SocketTransData.Type]
    E_DISTRIBUTE: SocketTransData.Type
    E_DP: SocketTransData.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    type: SocketTransData.Type
    distribute: _ble_pb2.BtAppMsg.Distribute
    def __init__(self, type: _Optional[_Union[SocketTransData.Type, str]] = ..., distribute: _Optional[_Union[_ble_pb2.BtAppMsg.Distribute, _Mapping]] = ...) -> None: ...
