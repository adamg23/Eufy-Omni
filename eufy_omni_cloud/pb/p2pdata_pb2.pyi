from . import common_pb2 as _common_pb2
from . import stream_pb2 as _stream_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapChannelMsg(_message.Message):
    __slots__ = ("type", "map_info", "multi_map_response")
    class MsgType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MAP_INFO: _ClassVar[MapChannelMsg.MsgType]
        MULTI_MAP_RESPONSE: _ClassVar[MapChannelMsg.MsgType]
    MAP_INFO: MapChannelMsg.MsgType
    MULTI_MAP_RESPONSE: MapChannelMsg.MsgType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_INFO_FIELD_NUMBER: _ClassVar[int]
    MULTI_MAP_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    type: MapChannelMsg.MsgType
    map_info: MapInfo
    multi_map_response: bytes
    def __init__(self, type: _Optional[_Union[MapChannelMsg.MsgType, str]] = ..., map_info: _Optional[_Union[MapInfo, _Mapping]] = ..., multi_map_response: _Optional[bytes] = ...) -> None: ...

class MapPixels(_message.Message):
    __slots__ = ("pixels", "pixel_size")
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    PIXEL_SIZE_FIELD_NUMBER: _ClassVar[int]
    pixels: bytes
    pixel_size: int
    def __init__(self, pixels: _Optional[bytes] = ..., pixel_size: _Optional[int] = ...) -> None: ...

class MapInfo(_message.Message):
    __slots__ = ("releases", "map_id", "map_stable", "map_width", "map_height", "origin", "docks", "msg_type", "pixels", "obstacles", "restricted_zones", "room_params", "cruise_data", "temporary_data", "is_new_map", "name")
    class MapMsgType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MAP_REALTIME: _ClassVar[MapInfo.MapMsgType]
        MAP_ROOMOUTLINE: _ClassVar[MapInfo.MapMsgType]
        OBSTACLE_INFO: _ClassVar[MapInfo.MapMsgType]
        RESTRICT_ZONES: _ClassVar[MapInfo.MapMsgType]
        ROOM_PARAMS: _ClassVar[MapInfo.MapMsgType]
        CRUISE_DATA: _ClassVar[MapInfo.MapMsgType]
        TEMPORARY_DATA: _ClassVar[MapInfo.MapMsgType]
    MAP_REALTIME: MapInfo.MapMsgType
    MAP_ROOMOUTLINE: MapInfo.MapMsgType
    OBSTACLE_INFO: MapInfo.MapMsgType
    RESTRICT_ZONES: MapInfo.MapMsgType
    ROOM_PARAMS: MapInfo.MapMsgType
    CRUISE_DATA: MapInfo.MapMsgType
    TEMPORARY_DATA: MapInfo.MapMsgType
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    MAP_STABLE_FIELD_NUMBER: _ClassVar[int]
    MAP_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MAP_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    DOCKS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    OBSTACLES_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_ZONES_FIELD_NUMBER: _ClassVar[int]
    ROOM_PARAMS_FIELD_NUMBER: _ClassVar[int]
    CRUISE_DATA_FIELD_NUMBER: _ClassVar[int]
    TEMPORARY_DATA_FIELD_NUMBER: _ClassVar[int]
    IS_NEW_MAP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    releases: int
    map_id: int
    map_stable: bool
    map_width: int
    map_height: int
    origin: _common_pb2.Point
    docks: _containers.RepeatedCompositeFieldContainer[_common_pb2.Pose]
    msg_type: MapInfo.MapMsgType
    pixels: MapPixels
    obstacles: _stream_pb2.ObstacleInfo
    restricted_zones: _stream_pb2.RestrictedZone
    room_params: _stream_pb2.RoomParams
    cruise_data: _stream_pb2.CruiseData
    temporary_data: _stream_pb2.TemporaryData
    is_new_map: int
    name: str
    def __init__(self, releases: _Optional[int] = ..., map_id: _Optional[int] = ..., map_stable: _Optional[bool] = ..., map_width: _Optional[int] = ..., map_height: _Optional[int] = ..., origin: _Optional[_Union[_common_pb2.Point, _Mapping]] = ..., docks: _Optional[_Iterable[_Union[_common_pb2.Pose, _Mapping]]] = ..., msg_type: _Optional[_Union[MapInfo.MapMsgType, str]] = ..., pixels: _Optional[_Union[MapPixels, _Mapping]] = ..., obstacles: _Optional[_Union[_stream_pb2.ObstacleInfo, _Mapping]] = ..., restricted_zones: _Optional[_Union[_stream_pb2.RestrictedZone, _Mapping]] = ..., room_params: _Optional[_Union[_stream_pb2.RoomParams, _Mapping]] = ..., cruise_data: _Optional[_Union[_stream_pb2.CruiseData, _Mapping]] = ..., temporary_data: _Optional[_Union[_stream_pb2.TemporaryData, _Mapping]] = ..., is_new_map: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class CompleteMap(_message.Message):
    __slots__ = ("releases", "map_id", "map_stable", "map_width", "map_height", "origin", "docks", "map", "room_outline", "obstacles", "restricted_zones", "room_params", "temporary_data", "is_new_map", "name")
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    MAP_STABLE_FIELD_NUMBER: _ClassVar[int]
    MAP_WIDTH_FIELD_NUMBER: _ClassVar[int]
    MAP_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    DOCKS_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    ROOM_OUTLINE_FIELD_NUMBER: _ClassVar[int]
    OBSTACLES_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_ZONES_FIELD_NUMBER: _ClassVar[int]
    ROOM_PARAMS_FIELD_NUMBER: _ClassVar[int]
    TEMPORARY_DATA_FIELD_NUMBER: _ClassVar[int]
    IS_NEW_MAP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    releases: int
    map_id: int
    map_stable: bool
    map_width: int
    map_height: int
    origin: _common_pb2.Point
    docks: _containers.RepeatedCompositeFieldContainer[_common_pb2.Pose]
    map: MapPixels
    room_outline: MapPixels
    obstacles: _stream_pb2.ObstacleInfo
    restricted_zones: _stream_pb2.RestrictedZone
    room_params: _stream_pb2.RoomParams
    temporary_data: _stream_pb2.TemporaryData
    is_new_map: int
    name: str
    def __init__(self, releases: _Optional[int] = ..., map_id: _Optional[int] = ..., map_stable: _Optional[bool] = ..., map_width: _Optional[int] = ..., map_height: _Optional[int] = ..., origin: _Optional[_Union[_common_pb2.Point, _Mapping]] = ..., docks: _Optional[_Iterable[_Union[_common_pb2.Pose, _Mapping]]] = ..., map: _Optional[_Union[MapPixels, _Mapping]] = ..., room_outline: _Optional[_Union[MapPixels, _Mapping]] = ..., obstacles: _Optional[_Union[_stream_pb2.ObstacleInfo, _Mapping]] = ..., restricted_zones: _Optional[_Union[_stream_pb2.RestrictedZone, _Mapping]] = ..., room_params: _Optional[_Union[_stream_pb2.RoomParams, _Mapping]] = ..., temporary_data: _Optional[_Union[_stream_pb2.TemporaryData, _Mapping]] = ..., is_new_map: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class CompletePath(_message.Message):
    __slots__ = ("path", "path_lz4len")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SWEEP: _ClassVar[CompletePath.Type]
        MOP: _ClassVar[CompletePath.Type]
        SWEEP_MOP: _ClassVar[CompletePath.Type]
        NAVI: _ClassVar[CompletePath.Type]
        GOHOME: _ClassVar[CompletePath.Type]
    SWEEP: CompletePath.Type
    MOP: CompletePath.Type
    SWEEP_MOP: CompletePath.Type
    NAVI: CompletePath.Type
    GOHOME: CompletePath.Type
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FOLLOW: _ClassVar[CompletePath.State]
        NEW: _ClassVar[CompletePath.State]
    FOLLOW: CompletePath.State
    NEW: CompletePath.State
    PATH_FIELD_NUMBER: _ClassVar[int]
    PATH_LZ4LEN_FIELD_NUMBER: _ClassVar[int]
    path: bytes
    path_lz4len: int
    def __init__(self, path: _Optional[bytes] = ..., path_lz4len: _Optional[int] = ...) -> None: ...
