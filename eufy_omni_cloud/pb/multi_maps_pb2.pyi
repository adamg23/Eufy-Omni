from . import common_pb2 as _common_pb2
from . import p2pdata_pb2 as _p2pdata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiMapsManageRequest(_message.Message):
    __slots__ = ("method", "seq", "rename", "common", "save_options")
    class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MAP_RESET: _ClassVar[MultiMapsManageRequest.Method]
        MAP_RENAME: _ClassVar[MultiMapsManageRequest.Method]
        MAP_LOAD: _ClassVar[MultiMapsManageRequest.Method]
        MAP_REPLACE: _ClassVar[MultiMapsManageRequest.Method]
        MAP_DELETE: _ClassVar[MultiMapsManageRequest.Method]
        MAP_SAVE: _ClassVar[MultiMapsManageRequest.Method]
        MAP_IGNORE: _ClassVar[MultiMapsManageRequest.Method]
        MAP_GET_ALL: _ClassVar[MultiMapsManageRequest.Method]
        MAP_GET_ONE: _ClassVar[MultiMapsManageRequest.Method]
        MAP_RECOVERY: _ClassVar[MultiMapsManageRequest.Method]
    MAP_RESET: MultiMapsManageRequest.Method
    MAP_RENAME: MultiMapsManageRequest.Method
    MAP_LOAD: MultiMapsManageRequest.Method
    MAP_REPLACE: MultiMapsManageRequest.Method
    MAP_DELETE: MultiMapsManageRequest.Method
    MAP_SAVE: MultiMapsManageRequest.Method
    MAP_IGNORE: MultiMapsManageRequest.Method
    MAP_GET_ALL: MultiMapsManageRequest.Method
    MAP_GET_ONE: MultiMapsManageRequest.Method
    MAP_RECOVERY: MultiMapsManageRequest.Method
    class Rename(_message.Message):
        __slots__ = ("cloud_mapid", "new_name")
        CLOUD_MAPID_FIELD_NUMBER: _ClassVar[int]
        NEW_NAME_FIELD_NUMBER: _ClassVar[int]
        cloud_mapid: int
        new_name: str
        def __init__(self, cloud_mapid: _Optional[int] = ..., new_name: _Optional[str] = ...) -> None: ...
    class Common(_message.Message):
        __slots__ = ("cloud_mapid",)
        CLOUD_MAPID_FIELD_NUMBER: _ClassVar[int]
        cloud_mapid: int
        def __init__(self, cloud_mapid: _Optional[int] = ...) -> None: ...
    class SaveOptions(_message.Message):
        __slots__ = ("multi_map_sw",)
        MULTI_MAP_SW_FIELD_NUMBER: _ClassVar[int]
        multi_map_sw: _common_pb2.Switch
        def __init__(self, multi_map_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    RENAME_FIELD_NUMBER: _ClassVar[int]
    COMMON_FIELD_NUMBER: _ClassVar[int]
    SAVE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    method: MultiMapsManageRequest.Method
    seq: int
    rename: MultiMapsManageRequest.Rename
    common: MultiMapsManageRequest.Common
    save_options: MultiMapsManageRequest.SaveOptions
    def __init__(self, method: _Optional[_Union[MultiMapsManageRequest.Method, str]] = ..., seq: _Optional[int] = ..., rename: _Optional[_Union[MultiMapsManageRequest.Rename, _Mapping]] = ..., common: _Optional[_Union[MultiMapsManageRequest.Common, _Mapping]] = ..., save_options: _Optional[_Union[MultiMapsManageRequest.SaveOptions, _Mapping]] = ...) -> None: ...

class MultiMapsManageResponse(_message.Message):
    __slots__ = ("method", "seq", "result", "map_infos", "complete_maps")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[MultiMapsManageResponse.Result]
        FAILED: _ClassVar[MultiMapsManageResponse.Result]
        STARTED: _ClassVar[MultiMapsManageResponse.Result]
    SUCCESS: MultiMapsManageResponse.Result
    FAILED: MultiMapsManageResponse.Result
    STARTED: MultiMapsManageResponse.Result
    class CompleteMaps(_message.Message):
        __slots__ = ("complete_map",)
        COMPLETE_MAP_FIELD_NUMBER: _ClassVar[int]
        complete_map: _containers.RepeatedCompositeFieldContainer[_p2pdata_pb2.CompleteMap]
        def __init__(self, complete_map: _Optional[_Iterable[_Union[_p2pdata_pb2.CompleteMap, _Mapping]]] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MAP_INFOS_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_MAPS_FIELD_NUMBER: _ClassVar[int]
    method: MultiMapsManageRequest.Method
    seq: int
    result: MultiMapsManageResponse.Result
    map_infos: _p2pdata_pb2.MapInfo
    complete_maps: MultiMapsManageResponse.CompleteMaps
    def __init__(self, method: _Optional[_Union[MultiMapsManageRequest.Method, str]] = ..., seq: _Optional[int] = ..., result: _Optional[_Union[MultiMapsManageResponse.Result, str]] = ..., map_infos: _Optional[_Union[_p2pdata_pb2.MapInfo, _Mapping]] = ..., complete_maps: _Optional[_Union[MultiMapsManageResponse.CompleteMaps, _Mapping]] = ...) -> None: ...
