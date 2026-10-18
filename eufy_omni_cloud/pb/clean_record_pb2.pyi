from . import clean_param_pb2 as _clean_param_pb2
from . import stream_pb2 as _stream_pb2
from . import p2pdata_pb2 as _p2pdata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CleanRecordDesc(_message.Message):
    __slots__ = ("start_time", "end_time", "duration", "area", "clean_type", "finish_reason", "extra")
    class FinishReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COMPLETED: _ClassVar[CleanRecordDesc.FinishReason]
        MANUDAL: _ClassVar[CleanRecordDesc.FinishReason]
        LOW_POWER: _ClassVar[CleanRecordDesc.FinishReason]
        EXCEPTION: _ClassVar[CleanRecordDesc.FinishReason]
    COMPLETED: CleanRecordDesc.FinishReason
    MANUDAL: CleanRecordDesc.FinishReason
    LOW_POWER: CleanRecordDesc.FinishReason
    EXCEPTION: CleanRecordDesc.FinishReason
    class Extra(_message.Message):
        __slots__ = ("mode", "mus", "error_code", "prompt_code")
        class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            AUTO: _ClassVar[CleanRecordDesc.Extra.Mode]
            SELECT_ROOM: _ClassVar[CleanRecordDesc.Extra.Mode]
            SELECT_ZONE: _ClassVar[CleanRecordDesc.Extra.Mode]
            SPOT: _ClassVar[CleanRecordDesc.Extra.Mode]
            SCHEDULE_AUTO_CLEAN: _ClassVar[CleanRecordDesc.Extra.Mode]
            SCHEDULE_ROOMS_CLEAN: _ClassVar[CleanRecordDesc.Extra.Mode]
        AUTO: CleanRecordDesc.Extra.Mode
        SELECT_ROOM: CleanRecordDesc.Extra.Mode
        SELECT_ZONE: CleanRecordDesc.Extra.Mode
        SPOT: CleanRecordDesc.Extra.Mode
        SCHEDULE_AUTO_CLEAN: CleanRecordDesc.Extra.Mode
        SCHEDULE_ROOMS_CLEAN: CleanRecordDesc.Extra.Mode
        MODE_FIELD_NUMBER: _ClassVar[int]
        MUS_FIELD_NUMBER: _ClassVar[int]
        ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
        PROMPT_CODE_FIELD_NUMBER: _ClassVar[int]
        mode: CleanRecordDesc.Extra.Mode
        mus: int
        error_code: int
        prompt_code: int
        def __init__(self, mode: _Optional[_Union[CleanRecordDesc.Extra.Mode, str]] = ..., mus: _Optional[int] = ..., error_code: _Optional[int] = ..., prompt_code: _Optional[int] = ...) -> None: ...
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    AREA_FIELD_NUMBER: _ClassVar[int]
    CLEAN_TYPE_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    start_time: int
    end_time: int
    duration: int
    area: int
    clean_type: _clean_param_pb2.CleanType
    finish_reason: CleanRecordDesc.FinishReason
    extra: CleanRecordDesc.Extra
    def __init__(self, start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., duration: _Optional[int] = ..., area: _Optional[int] = ..., clean_type: _Optional[_Union[_clean_param_pb2.CleanType, _Mapping]] = ..., finish_reason: _Optional[_Union[CleanRecordDesc.FinishReason, str]] = ..., extra: _Optional[_Union[CleanRecordDesc.Extra, _Mapping]] = ...) -> None: ...

class CleanRecordData(_message.Message):
    __slots__ = ("restricted_zone", "temp_data", "room_params", "path_data", "map", "room_outline", "obstacle_info", "path_data_v2", "map_p2p", "path_p2p")
    class PathData(_message.Message):
        __slots__ = ("points",)
        POINTS_FIELD_NUMBER: _ClassVar[int]
        points: _containers.RepeatedCompositeFieldContainer[_stream_pb2.PathPoint]
        def __init__(self, points: _Optional[_Iterable[_Union[_stream_pb2.PathPoint, _Mapping]]] = ...) -> None: ...
    RESTRICTED_ZONE_FIELD_NUMBER: _ClassVar[int]
    TEMP_DATA_FIELD_NUMBER: _ClassVar[int]
    ROOM_PARAMS_FIELD_NUMBER: _ClassVar[int]
    PATH_DATA_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    ROOM_OUTLINE_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_INFO_FIELD_NUMBER: _ClassVar[int]
    PATH_DATA_V2_FIELD_NUMBER: _ClassVar[int]
    MAP_P2P_FIELD_NUMBER: _ClassVar[int]
    PATH_P2P_FIELD_NUMBER: _ClassVar[int]
    restricted_zone: _stream_pb2.RestrictedZone
    temp_data: _stream_pb2.TemporaryData
    room_params: _stream_pb2.RoomParams
    path_data: bytes
    map: _stream_pb2.Map
    room_outline: _stream_pb2.RoomOutline
    obstacle_info: _stream_pb2.ObstacleInfo
    path_data_v2: CleanRecordData.PathData
    map_p2p: _p2pdata_pb2.CompleteMap
    path_p2p: _p2pdata_pb2.CompletePath
    def __init__(self, restricted_zone: _Optional[_Union[_stream_pb2.RestrictedZone, _Mapping]] = ..., temp_data: _Optional[_Union[_stream_pb2.TemporaryData, _Mapping]] = ..., room_params: _Optional[_Union[_stream_pb2.RoomParams, _Mapping]] = ..., path_data: _Optional[bytes] = ..., map: _Optional[_Union[_stream_pb2.Map, _Mapping]] = ..., room_outline: _Optional[_Union[_stream_pb2.RoomOutline, _Mapping]] = ..., obstacle_info: _Optional[_Union[_stream_pb2.ObstacleInfo, _Mapping]] = ..., path_data_v2: _Optional[_Union[CleanRecordData.PathData, _Mapping]] = ..., map_p2p: _Optional[_Union[_p2pdata_pb2.CompleteMap, _Mapping]] = ..., path_p2p: _Optional[_Union[_p2pdata_pb2.CompletePath, _Mapping]] = ...) -> None: ...

class CruiseRecordDesc(_message.Message):
    __slots__ = ("start_time", "end_time", "duration", "finish_reason", "extra")
    class FinishReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COMPLETED: _ClassVar[CruiseRecordDesc.FinishReason]
        MANUDAL: _ClassVar[CruiseRecordDesc.FinishReason]
        LOW_POWER: _ClassVar[CruiseRecordDesc.FinishReason]
        EXCEPTION: _ClassVar[CruiseRecordDesc.FinishReason]
    COMPLETED: CruiseRecordDesc.FinishReason
    MANUDAL: CruiseRecordDesc.FinishReason
    LOW_POWER: CruiseRecordDesc.FinishReason
    EXCEPTION: CruiseRecordDesc.FinishReason
    class Extra(_message.Message):
        __slots__ = ("mode",)
        class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            GLOBAL_CRUISE: _ClassVar[CruiseRecordDesc.Extra.Mode]
            POINT_CRUISE: _ClassVar[CruiseRecordDesc.Extra.Mode]
            ZONES_CRUISE: _ClassVar[CruiseRecordDesc.Extra.Mode]
            SCHEDULE_CRUISE: _ClassVar[CruiseRecordDesc.Extra.Mode]
        GLOBAL_CRUISE: CruiseRecordDesc.Extra.Mode
        POINT_CRUISE: CruiseRecordDesc.Extra.Mode
        ZONES_CRUISE: CruiseRecordDesc.Extra.Mode
        SCHEDULE_CRUISE: CruiseRecordDesc.Extra.Mode
        MODE_FIELD_NUMBER: _ClassVar[int]
        mode: CruiseRecordDesc.Extra.Mode
        def __init__(self, mode: _Optional[_Union[CruiseRecordDesc.Extra.Mode, str]] = ...) -> None: ...
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    start_time: int
    end_time: int
    duration: int
    finish_reason: CruiseRecordDesc.FinishReason
    extra: CruiseRecordDesc.Extra
    def __init__(self, start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., duration: _Optional[int] = ..., finish_reason: _Optional[_Union[CruiseRecordDesc.FinishReason, str]] = ..., extra: _Optional[_Union[CruiseRecordDesc.Extra, _Mapping]] = ...) -> None: ...

class CruiseRecordData(_message.Message):
    __slots__ = ("restricted_zone", "temp_data", "room_params", "obstacle_info", "path_data", "cruise_data", "map", "room_outline", "map_p2p", "path_p2p")
    RESTRICTED_ZONE_FIELD_NUMBER: _ClassVar[int]
    TEMP_DATA_FIELD_NUMBER: _ClassVar[int]
    ROOM_PARAMS_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_INFO_FIELD_NUMBER: _ClassVar[int]
    PATH_DATA_FIELD_NUMBER: _ClassVar[int]
    CRUISE_DATA_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    ROOM_OUTLINE_FIELD_NUMBER: _ClassVar[int]
    MAP_P2P_FIELD_NUMBER: _ClassVar[int]
    PATH_P2P_FIELD_NUMBER: _ClassVar[int]
    restricted_zone: _stream_pb2.RestrictedZone
    temp_data: _stream_pb2.TemporaryData
    room_params: _stream_pb2.RoomParams
    obstacle_info: _stream_pb2.ObstacleInfo
    path_data: bytes
    cruise_data: _stream_pb2.CruiseData
    map: _stream_pb2.Map
    room_outline: _stream_pb2.RoomOutline
    map_p2p: _p2pdata_pb2.CompleteMap
    path_p2p: _p2pdata_pb2.CompletePath
    def __init__(self, restricted_zone: _Optional[_Union[_stream_pb2.RestrictedZone, _Mapping]] = ..., temp_data: _Optional[_Union[_stream_pb2.TemporaryData, _Mapping]] = ..., room_params: _Optional[_Union[_stream_pb2.RoomParams, _Mapping]] = ..., obstacle_info: _Optional[_Union[_stream_pb2.ObstacleInfo, _Mapping]] = ..., path_data: _Optional[bytes] = ..., cruise_data: _Optional[_Union[_stream_pb2.CruiseData, _Mapping]] = ..., map: _Optional[_Union[_stream_pb2.Map, _Mapping]] = ..., room_outline: _Optional[_Union[_stream_pb2.RoomOutline, _Mapping]] = ..., map_p2p: _Optional[_Union[_p2pdata_pb2.CompleteMap, _Mapping]] = ..., path_p2p: _Optional[_Union[_p2pdata_pb2.CompletePath, _Mapping]] = ...) -> None: ...
