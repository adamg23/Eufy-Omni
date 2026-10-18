from . import common_pb2 as _common_pb2
from . import clean_param_pb2 as _clean_param_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RemoteCtrl(_message.Message):
    __slots__ = ("direction",)
    class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BRAKE: _ClassVar[RemoteCtrl.Direction]
        FORWARD: _ClassVar[RemoteCtrl.Direction]
        BACK: _ClassVar[RemoteCtrl.Direction]
        LEFT: _ClassVar[RemoteCtrl.Direction]
        RIGHT: _ClassVar[RemoteCtrl.Direction]
    BRAKE: RemoteCtrl.Direction
    FORWARD: RemoteCtrl.Direction
    BACK: RemoteCtrl.Direction
    LEFT: RemoteCtrl.Direction
    RIGHT: RemoteCtrl.Direction
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    direction: RemoteCtrl.Direction
    def __init__(self, direction: _Optional[_Union[RemoteCtrl.Direction, str]] = ...) -> None: ...

class AutoClean(_message.Message):
    __slots__ = ("clean_times", "force_mapping")
    CLEAN_TIMES_FIELD_NUMBER: _ClassVar[int]
    FORCE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    clean_times: int
    force_mapping: bool
    def __init__(self, clean_times: _Optional[int] = ..., force_mapping: _Optional[bool] = ...) -> None: ...

class SelectRoomsClean(_message.Message):
    __slots__ = ("rooms", "clean_times", "map_id", "releases", "mode")
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        GENERAL: _ClassVar[SelectRoomsClean.Mode]
        CUSTOMIZE: _ClassVar[SelectRoomsClean.Mode]
    GENERAL: SelectRoomsClean.Mode
    CUSTOMIZE: SelectRoomsClean.Mode
    class Room(_message.Message):
        __slots__ = ("id", "order")
        ID_FIELD_NUMBER: _ClassVar[int]
        ORDER_FIELD_NUMBER: _ClassVar[int]
        id: int
        order: int
        def __init__(self, id: _Optional[int] = ..., order: _Optional[int] = ...) -> None: ...
    ROOMS_FIELD_NUMBER: _ClassVar[int]
    CLEAN_TIMES_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    rooms: _containers.RepeatedCompositeFieldContainer[SelectRoomsClean.Room]
    clean_times: int
    map_id: int
    releases: int
    mode: SelectRoomsClean.Mode
    def __init__(self, rooms: _Optional[_Iterable[_Union[SelectRoomsClean.Room, _Mapping]]] = ..., clean_times: _Optional[int] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ..., mode: _Optional[_Union[SelectRoomsClean.Mode, str]] = ...) -> None: ...

class SelectZonesClean(_message.Message):
    __slots__ = ("zones", "map_id", "releases", "type")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NORMAL: _ClassVar[SelectZonesClean.Type]
        POOP_CLEANING: _ClassVar[SelectZonesClean.Type]
    NORMAL: SelectZonesClean.Type
    POOP_CLEANING: SelectZonesClean.Type
    class Zone(_message.Message):
        __slots__ = ("quadrangle", "clean_times")
        QUADRANGLE_FIELD_NUMBER: _ClassVar[int]
        CLEAN_TIMES_FIELD_NUMBER: _ClassVar[int]
        quadrangle: _common_pb2.Quadrangle
        clean_times: int
        def __init__(self, quadrangle: _Optional[_Union[_common_pb2.Quadrangle, _Mapping]] = ..., clean_times: _Optional[int] = ...) -> None: ...
    ZONES_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    zones: _containers.RepeatedCompositeFieldContainer[SelectZonesClean.Zone]
    map_id: int
    releases: int
    type: SelectZonesClean.Type
    def __init__(self, zones: _Optional[_Iterable[_Union[SelectZonesClean.Zone, _Mapping]]] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ..., type: _Optional[_Union[SelectZonesClean.Type, str]] = ...) -> None: ...

class SceneClean(_message.Message):
    __slots__ = ("scene_id",)
    SCENE_ID_FIELD_NUMBER: _ClassVar[int]
    scene_id: int
    def __init__(self, scene_id: _Optional[int] = ...) -> None: ...

class SpotClean(_message.Message):
    __slots__ = ("clean_times",)
    CLEAN_TIMES_FIELD_NUMBER: _ClassVar[int]
    clean_times: int
    def __init__(self, clean_times: _Optional[int] = ...) -> None: ...

class Goto(_message.Message):
    __slots__ = ("destination", "type", "clean_times", "map_id", "releases")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        GOTO_DESTINATION: _ClassVar[Goto.Type]
        GOTO_SPOT: _ClassVar[Goto.Type]
        GOTO_AUTO: _ClassVar[Goto.Type]
    GOTO_DESTINATION: Goto.Type
    GOTO_SPOT: Goto.Type
    GOTO_AUTO: Goto.Type
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CLEAN_TIMES_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    destination: _common_pb2.Point
    type: Goto.Type
    clean_times: int
    map_id: int
    releases: int
    def __init__(self, destination: _Optional[_Union[_common_pb2.Point, _Mapping]] = ..., type: _Optional[_Union[Goto.Type, str]] = ..., clean_times: _Optional[int] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ...) -> None: ...

class ScheduleAutoClean(_message.Message):
    __slots__ = ("fan", "mop_mode", "clean_type", "clean_extent")
    FAN_FIELD_NUMBER: _ClassVar[int]
    MOP_MODE_FIELD_NUMBER: _ClassVar[int]
    CLEAN_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLEAN_EXTENT_FIELD_NUMBER: _ClassVar[int]
    fan: _clean_param_pb2.Fan
    mop_mode: _clean_param_pb2.MopMode
    clean_type: _clean_param_pb2.CleanType
    clean_extent: _clean_param_pb2.CleanExtent
    def __init__(self, fan: _Optional[_Union[_clean_param_pb2.Fan, _Mapping]] = ..., mop_mode: _Optional[_Union[_clean_param_pb2.MopMode, _Mapping]] = ..., clean_type: _Optional[_Union[_clean_param_pb2.CleanType, _Mapping]] = ..., clean_extent: _Optional[_Union[_clean_param_pb2.CleanExtent, _Mapping]] = ...) -> None: ...

class ScheduleRoomsClean(_message.Message):
    __slots__ = ("fan", "mop_mode", "clean_type", "clean_extent", "rooms", "map_id", "releases")
    class Room(_message.Message):
        __slots__ = ("id", "order")
        ID_FIELD_NUMBER: _ClassVar[int]
        ORDER_FIELD_NUMBER: _ClassVar[int]
        id: int
        order: int
        def __init__(self, id: _Optional[int] = ..., order: _Optional[int] = ...) -> None: ...
    FAN_FIELD_NUMBER: _ClassVar[int]
    MOP_MODE_FIELD_NUMBER: _ClassVar[int]
    CLEAN_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLEAN_EXTENT_FIELD_NUMBER: _ClassVar[int]
    ROOMS_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    fan: _clean_param_pb2.Fan
    mop_mode: _clean_param_pb2.MopMode
    clean_type: _clean_param_pb2.CleanType
    clean_extent: _clean_param_pb2.CleanExtent
    rooms: _containers.RepeatedCompositeFieldContainer[ScheduleRoomsClean.Room]
    map_id: int
    releases: int
    def __init__(self, fan: _Optional[_Union[_clean_param_pb2.Fan, _Mapping]] = ..., mop_mode: _Optional[_Union[_clean_param_pb2.MopMode, _Mapping]] = ..., clean_type: _Optional[_Union[_clean_param_pb2.CleanType, _Mapping]] = ..., clean_extent: _Optional[_Union[_clean_param_pb2.CleanExtent, _Mapping]] = ..., rooms: _Optional[_Iterable[_Union[ScheduleRoomsClean.Room, _Mapping]]] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ...) -> None: ...

class GlobalCruise(_message.Message):
    __slots__ = ("map_id", "releases")
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    map_id: int
    releases: int
    def __init__(self, map_id: _Optional[int] = ..., releases: _Optional[int] = ...) -> None: ...

class PointCruise(_message.Message):
    __slots__ = ("points", "map_id", "releases")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    points: _common_pb2.Point
    map_id: int
    releases: int
    def __init__(self, points: _Optional[_Union[_common_pb2.Point, _Mapping]] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ...) -> None: ...

class ZonesCruise(_message.Message):
    __slots__ = ("points", "map_id", "releases")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[_common_pb2.Point]
    map_id: int
    releases: int
    def __init__(self, points: _Optional[_Iterable[_Union[_common_pb2.Point, _Mapping]]] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ...) -> None: ...

class ScheduleCruise(_message.Message):
    __slots__ = ("map_id", "releases")
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    map_id: int
    releases: int
    def __init__(self, map_id: _Optional[int] = ..., releases: _Optional[int] = ...) -> None: ...

class ModeCtrlRequest(_message.Message):
    __slots__ = ("method", "seq", "auto_clean", "select_rooms_clean", "select_zones_clean", "spot_clean", "go_to", "sche_auto_clean", "sche_rooms_clean", "global_cruise", "point_cruise", "zones_cruise", "sche_cruise", "scene_clean")
    class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        START_AUTO_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_SELECT_ROOMS_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_SELECT_ZONES_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_SPOT_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_GOTO_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_RC_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_GOHOME: _ClassVar[ModeCtrlRequest.Method]
        START_SCHEDULE_AUTO_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_SCHEDULE_ROOMS_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_FAST_MAPPING: _ClassVar[ModeCtrlRequest.Method]
        START_GOWASH: _ClassVar[ModeCtrlRequest.Method]
        STOP_TASK: _ClassVar[ModeCtrlRequest.Method]
        PAUSE_TASK: _ClassVar[ModeCtrlRequest.Method]
        RESUME_TASK: _ClassVar[ModeCtrlRequest.Method]
        STOP_GOHOME: _ClassVar[ModeCtrlRequest.Method]
        STOP_RC_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        STOP_GOWASH: _ClassVar[ModeCtrlRequest.Method]
        STOP_SMART_FOLLOW: _ClassVar[ModeCtrlRequest.Method]
        START_GLOBAL_CRUISE: _ClassVar[ModeCtrlRequest.Method]
        START_POINT_CRUISE: _ClassVar[ModeCtrlRequest.Method]
        START_ZONES_CRUISE: _ClassVar[ModeCtrlRequest.Method]
        START_SCHEDULE_CRUISE: _ClassVar[ModeCtrlRequest.Method]
        START_SCENE_CLEAN: _ClassVar[ModeCtrlRequest.Method]
        START_MAPPING_THEN_CLEAN: _ClassVar[ModeCtrlRequest.Method]
    START_AUTO_CLEAN: ModeCtrlRequest.Method
    START_SELECT_ROOMS_CLEAN: ModeCtrlRequest.Method
    START_SELECT_ZONES_CLEAN: ModeCtrlRequest.Method
    START_SPOT_CLEAN: ModeCtrlRequest.Method
    START_GOTO_CLEAN: ModeCtrlRequest.Method
    START_RC_CLEAN: ModeCtrlRequest.Method
    START_GOHOME: ModeCtrlRequest.Method
    START_SCHEDULE_AUTO_CLEAN: ModeCtrlRequest.Method
    START_SCHEDULE_ROOMS_CLEAN: ModeCtrlRequest.Method
    START_FAST_MAPPING: ModeCtrlRequest.Method
    START_GOWASH: ModeCtrlRequest.Method
    STOP_TASK: ModeCtrlRequest.Method
    PAUSE_TASK: ModeCtrlRequest.Method
    RESUME_TASK: ModeCtrlRequest.Method
    STOP_GOHOME: ModeCtrlRequest.Method
    STOP_RC_CLEAN: ModeCtrlRequest.Method
    STOP_GOWASH: ModeCtrlRequest.Method
    STOP_SMART_FOLLOW: ModeCtrlRequest.Method
    START_GLOBAL_CRUISE: ModeCtrlRequest.Method
    START_POINT_CRUISE: ModeCtrlRequest.Method
    START_ZONES_CRUISE: ModeCtrlRequest.Method
    START_SCHEDULE_CRUISE: ModeCtrlRequest.Method
    START_SCENE_CLEAN: ModeCtrlRequest.Method
    START_MAPPING_THEN_CLEAN: ModeCtrlRequest.Method
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    AUTO_CLEAN_FIELD_NUMBER: _ClassVar[int]
    SELECT_ROOMS_CLEAN_FIELD_NUMBER: _ClassVar[int]
    SELECT_ZONES_CLEAN_FIELD_NUMBER: _ClassVar[int]
    SPOT_CLEAN_FIELD_NUMBER: _ClassVar[int]
    GO_TO_FIELD_NUMBER: _ClassVar[int]
    SCHE_AUTO_CLEAN_FIELD_NUMBER: _ClassVar[int]
    SCHE_ROOMS_CLEAN_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_CRUISE_FIELD_NUMBER: _ClassVar[int]
    POINT_CRUISE_FIELD_NUMBER: _ClassVar[int]
    ZONES_CRUISE_FIELD_NUMBER: _ClassVar[int]
    SCHE_CRUISE_FIELD_NUMBER: _ClassVar[int]
    SCENE_CLEAN_FIELD_NUMBER: _ClassVar[int]
    method: ModeCtrlRequest.Method
    seq: int
    auto_clean: AutoClean
    select_rooms_clean: SelectRoomsClean
    select_zones_clean: SelectZonesClean
    spot_clean: SpotClean
    go_to: Goto
    sche_auto_clean: ScheduleAutoClean
    sche_rooms_clean: ScheduleRoomsClean
    global_cruise: GlobalCruise
    point_cruise: PointCruise
    zones_cruise: ZonesCruise
    sche_cruise: ScheduleCruise
    scene_clean: SceneClean
    def __init__(self, method: _Optional[_Union[ModeCtrlRequest.Method, str]] = ..., seq: _Optional[int] = ..., auto_clean: _Optional[_Union[AutoClean, _Mapping]] = ..., select_rooms_clean: _Optional[_Union[SelectRoomsClean, _Mapping]] = ..., select_zones_clean: _Optional[_Union[SelectZonesClean, _Mapping]] = ..., spot_clean: _Optional[_Union[SpotClean, _Mapping]] = ..., go_to: _Optional[_Union[Goto, _Mapping]] = ..., sche_auto_clean: _Optional[_Union[ScheduleAutoClean, _Mapping]] = ..., sche_rooms_clean: _Optional[_Union[ScheduleRoomsClean, _Mapping]] = ..., global_cruise: _Optional[_Union[GlobalCruise, _Mapping]] = ..., point_cruise: _Optional[_Union[PointCruise, _Mapping]] = ..., zones_cruise: _Optional[_Union[ZonesCruise, _Mapping]] = ..., sche_cruise: _Optional[_Union[ScheduleCruise, _Mapping]] = ..., scene_clean: _Optional[_Union[SceneClean, _Mapping]] = ...) -> None: ...

class ModeCtrlResponse(_message.Message):
    __slots__ = ("method", "seq", "result")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[ModeCtrlResponse.Result]
        FAILED: _ClassVar[ModeCtrlResponse.Result]
    SUCCESS: ModeCtrlResponse.Result
    FAILED: ModeCtrlResponse.Result
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    method: ModeCtrlRequest.Method
    seq: int
    result: ModeCtrlResponse.Result
    def __init__(self, method: _Optional[_Union[ModeCtrlRequest.Method, str]] = ..., seq: _Optional[int] = ..., result: _Optional[_Union[ModeCtrlResponse.Result, str]] = ...) -> None: ...
