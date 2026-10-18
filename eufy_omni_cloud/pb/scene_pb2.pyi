from . import common_pb2 as _common_pb2
from . import clean_param_pb2 as _clean_param_pb2
from . import timing_pb2 as _timing_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SceneTask(_message.Message):
    __slots__ = ("index", "type", "current_room", "all_rooms")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CURRENT_ROOM: _ClassVar[SceneTask.Type]
        ALL_ROOMS: _ClassVar[SceneTask.Type]
    CURRENT_ROOM: SceneTask.Type
    ALL_ROOMS: SceneTask.Type
    class CleanMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        GENERAL: _ClassVar[SceneTask.CleanMode]
        SMART: _ClassVar[SceneTask.CleanMode]
    GENERAL: SceneTask.CleanMode
    SMART: SceneTask.CleanMode
    class General(_message.Message):
        __slots__ = ("clean_type", "clean_times", "fan", "mop_mode", "clean_extent")
        CLEAN_TYPE_FIELD_NUMBER: _ClassVar[int]
        CLEAN_TIMES_FIELD_NUMBER: _ClassVar[int]
        FAN_FIELD_NUMBER: _ClassVar[int]
        MOP_MODE_FIELD_NUMBER: _ClassVar[int]
        CLEAN_EXTENT_FIELD_NUMBER: _ClassVar[int]
        clean_type: _clean_param_pb2.CleanType
        clean_times: int
        fan: _clean_param_pb2.Fan
        mop_mode: _clean_param_pb2.MopMode
        clean_extent: _clean_param_pb2.CleanExtent
        def __init__(self, clean_type: _Optional[_Union[_clean_param_pb2.CleanType, _Mapping]] = ..., clean_times: _Optional[int] = ..., fan: _Optional[_Union[_clean_param_pb2.Fan, _Mapping]] = ..., mop_mode: _Optional[_Union[_clean_param_pb2.MopMode, _Mapping]] = ..., clean_extent: _Optional[_Union[_clean_param_pb2.CleanExtent, _Mapping]] = ...) -> None: ...
    class CurrentRoom(_message.Message):
        __slots__ = ("mode", "units")
        class Unit(_message.Message):
            __slots__ = ("general", "room_clean", "zone_clean")
            class RoomClean(_message.Message):
                __slots__ = ("room_id", "room_scene")
                ROOM_ID_FIELD_NUMBER: _ClassVar[int]
                ROOM_SCENE_FIELD_NUMBER: _ClassVar[int]
                room_id: int
                room_scene: _common_pb2.RoomScene
                def __init__(self, room_id: _Optional[int] = ..., room_scene: _Optional[_Union[_common_pb2.RoomScene, _Mapping]] = ...) -> None: ...
            class ZoneClean(_message.Message):
                __slots__ = ("quadrangle",)
                QUADRANGLE_FIELD_NUMBER: _ClassVar[int]
                quadrangle: _common_pb2.Quadrangle
                def __init__(self, quadrangle: _Optional[_Union[_common_pb2.Quadrangle, _Mapping]] = ...) -> None: ...
            GENERAL_FIELD_NUMBER: _ClassVar[int]
            ROOM_CLEAN_FIELD_NUMBER: _ClassVar[int]
            ZONE_CLEAN_FIELD_NUMBER: _ClassVar[int]
            general: SceneTask.General
            room_clean: SceneTask.CurrentRoom.Unit.RoomClean
            zone_clean: SceneTask.CurrentRoom.Unit.ZoneClean
            def __init__(self, general: _Optional[_Union[SceneTask.General, _Mapping]] = ..., room_clean: _Optional[_Union[SceneTask.CurrentRoom.Unit.RoomClean, _Mapping]] = ..., zone_clean: _Optional[_Union[SceneTask.CurrentRoom.Unit.ZoneClean, _Mapping]] = ...) -> None: ...
        MODE_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        mode: SceneTask.CleanMode
        units: _containers.RepeatedCompositeFieldContainer[SceneTask.CurrentRoom.Unit]
        def __init__(self, mode: _Optional[_Union[SceneTask.CleanMode, str]] = ..., units: _Optional[_Iterable[_Union[SceneTask.CurrentRoom.Unit, _Mapping]]] = ...) -> None: ...
    class AllRooms(_message.Message):
        __slots__ = ("mode", "general")
        MODE_FIELD_NUMBER: _ClassVar[int]
        GENERAL_FIELD_NUMBER: _ClassVar[int]
        mode: SceneTask.CleanMode
        general: SceneTask.General
        def __init__(self, mode: _Optional[_Union[SceneTask.CleanMode, str]] = ..., general: _Optional[_Union[SceneTask.General, _Mapping]] = ...) -> None: ...
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ROOM_FIELD_NUMBER: _ClassVar[int]
    ALL_ROOMS_FIELD_NUMBER: _ClassVar[int]
    index: int
    type: SceneTask.Type
    current_room: SceneTask.CurrentRoom
    all_rooms: SceneTask.AllRooms
    def __init__(self, index: _Optional[int] = ..., type: _Optional[_Union[SceneTask.Type, str]] = ..., current_room: _Optional[_Union[SceneTask.CurrentRoom, _Mapping]] = ..., all_rooms: _Optional[_Union[SceneTask.AllRooms, _Mapping]] = ...) -> None: ...

class SceneInfo(_message.Message):
    __slots__ = ("id", "valid", "invalid_reason", "name", "mapid", "estimate_time", "index", "type")
    class InvalidReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NORMAL: _ClassVar[SceneInfo.InvalidReason]
        MAP_NOT_EXIST: _ClassVar[SceneInfo.InvalidReason]
        MAP_NOT_AVAILABLE: _ClassVar[SceneInfo.InvalidReason]
        MAP_NOT_MATCH: _ClassVar[SceneInfo.InvalidReason]
        OTHER: _ClassVar[SceneInfo.InvalidReason]
        DEFAULT: _ClassVar[SceneInfo.InvalidReason]
    NORMAL: SceneInfo.InvalidReason
    MAP_NOT_EXIST: SceneInfo.InvalidReason
    MAP_NOT_AVAILABLE: SceneInfo.InvalidReason
    MAP_NOT_MATCH: SceneInfo.InvalidReason
    OTHER: SceneInfo.InvalidReason
    DEFAULT: SceneInfo.InvalidReason
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SCENE_NORMAL: _ClassVar[SceneInfo.Type]
        WHOLE_HOUSE_DAILY_CLEANING: _ClassVar[SceneInfo.Type]
        WHOLE_HOUSE_DEEP_CLEANING: _ClassVar[SceneInfo.Type]
        AFTER_DINNER_CLEANING: _ClassVar[SceneInfo.Type]
        PET_AREA_CLEANING: _ClassVar[SceneInfo.Type]
    SCENE_NORMAL: SceneInfo.Type
    WHOLE_HOUSE_DAILY_CLEANING: SceneInfo.Type
    WHOLE_HOUSE_DEEP_CLEANING: SceneInfo.Type
    AFTER_DINNER_CLEANING: SceneInfo.Type
    PET_AREA_CLEANING: SceneInfo.Type
    class Id(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: int
        def __init__(self, value: _Optional[int] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    INVALID_REASON_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MAPID_FIELD_NUMBER: _ClassVar[int]
    ESTIMATE_TIME_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: SceneInfo.Id
    valid: bool
    invalid_reason: SceneInfo.InvalidReason
    name: str
    mapid: int
    estimate_time: int
    index: int
    type: SceneInfo.Type
    def __init__(self, id: _Optional[_Union[SceneInfo.Id, _Mapping]] = ..., valid: _Optional[bool] = ..., invalid_reason: _Optional[_Union[SceneInfo.InvalidReason, str]] = ..., name: _Optional[str] = ..., mapid: _Optional[int] = ..., estimate_time: _Optional[int] = ..., index: _Optional[int] = ..., type: _Optional[_Union[SceneInfo.Type, str]] = ...) -> None: ...

class SceneRequest(_message.Message):
    __slots__ = ("method", "seq", "common", "scene")
    class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT: _ClassVar[SceneRequest.Method]
        ADD_SCENE: _ClassVar[SceneRequest.Method]
        DELETE_SCENE: _ClassVar[SceneRequest.Method]
        MODIFY_SCENE: _ClassVar[SceneRequest.Method]
    DEFAULT: SceneRequest.Method
    ADD_SCENE: SceneRequest.Method
    DELETE_SCENE: SceneRequest.Method
    MODIFY_SCENE: SceneRequest.Method
    class Common(_message.Message):
        __slots__ = ("scene_id",)
        SCENE_ID_FIELD_NUMBER: _ClassVar[int]
        scene_id: int
        def __init__(self, scene_id: _Optional[int] = ...) -> None: ...
    class Scene(_message.Message):
        __slots__ = ("info", "tasks", "desc")
        INFO_FIELD_NUMBER: _ClassVar[int]
        TASKS_FIELD_NUMBER: _ClassVar[int]
        DESC_FIELD_NUMBER: _ClassVar[int]
        info: SceneInfo
        tasks: _containers.RepeatedCompositeFieldContainer[SceneTask]
        desc: _timing_pb2.TimerInfo.Desc
        def __init__(self, info: _Optional[_Union[SceneInfo, _Mapping]] = ..., tasks: _Optional[_Iterable[_Union[SceneTask, _Mapping]]] = ..., desc: _Optional[_Union[_timing_pb2.TimerInfo.Desc, _Mapping]] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    COMMON_FIELD_NUMBER: _ClassVar[int]
    SCENE_FIELD_NUMBER: _ClassVar[int]
    method: SceneRequest.Method
    seq: int
    common: SceneRequest.Common
    scene: SceneRequest.Scene
    def __init__(self, method: _Optional[_Union[SceneRequest.Method, str]] = ..., seq: _Optional[int] = ..., common: _Optional[_Union[SceneRequest.Common, _Mapping]] = ..., scene: _Optional[_Union[SceneRequest.Scene, _Mapping]] = ...) -> None: ...

class SceneResponse(_message.Message):
    __slots__ = ("method", "seq", "result", "infos")
    class Result(_message.Message):
        __slots__ = ("value", "err_code")
        class Value(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SUCCESS: _ClassVar[SceneResponse.Result.Value]
            FAILED: _ClassVar[SceneResponse.Result.Value]
        SUCCESS: SceneResponse.Result.Value
        FAILED: SceneResponse.Result.Value
        VALUE_FIELD_NUMBER: _ClassVar[int]
        ERR_CODE_FIELD_NUMBER: _ClassVar[int]
        value: SceneResponse.Result.Value
        err_code: int
        def __init__(self, value: _Optional[_Union[SceneResponse.Result.Value, str]] = ..., err_code: _Optional[int] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    INFOS_FIELD_NUMBER: _ClassVar[int]
    method: SceneRequest.Method
    seq: int
    result: SceneResponse.Result
    infos: _containers.RepeatedCompositeFieldContainer[SceneInfo]
    def __init__(self, method: _Optional[_Union[SceneRequest.Method, str]] = ..., seq: _Optional[int] = ..., result: _Optional[_Union[SceneResponse.Result, _Mapping]] = ..., infos: _Optional[_Iterable[_Union[SceneInfo, _Mapping]]] = ...) -> None: ...
