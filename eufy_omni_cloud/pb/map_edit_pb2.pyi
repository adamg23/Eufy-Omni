from . import common_pb2 as _common_pb2
from . import stream_pb2 as _stream_pb2
from . import clean_param_pb2 as _clean_param_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapEditRequest(_message.Message):
    __slots__ = ("method", "seq", "map_id", "merge_rooms", "divide_room", "restricted_zone", "room_desc", "rooms_custom", "cruise_points", "rotation", "ignore_obstacle")
    class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MERGE_ROOMS: _ClassVar[MapEditRequest.Method]
        DIVIDE_ROOM: _ClassVar[MapEditRequest.Method]
        RESET_ROOMS: _ClassVar[MapEditRequest.Method]
        RENAME_ROOM: _ClassVar[MapEditRequest.Method]
        SET_RESTRICTED_ZONES: _ClassVar[MapEditRequest.Method]
        SET_ROOMS_CUSTOM: _ClassVar[MapEditRequest.Method]
        SET_CRUISE_POINTS: _ClassVar[MapEditRequest.Method]
        ROTATION: _ClassVar[MapEditRequest.Method]
        IGNORE_OBSTACLE: _ClassVar[MapEditRequest.Method]
    MERGE_ROOMS: MapEditRequest.Method
    DIVIDE_ROOM: MapEditRequest.Method
    RESET_ROOMS: MapEditRequest.Method
    RENAME_ROOM: MapEditRequest.Method
    SET_RESTRICTED_ZONES: MapEditRequest.Method
    SET_ROOMS_CUSTOM: MapEditRequest.Method
    SET_CRUISE_POINTS: MapEditRequest.Method
    ROTATION: MapEditRequest.Method
    IGNORE_OBSTACLE: MapEditRequest.Method
    class MergeRooms(_message.Message):
        __slots__ = ("room_ids",)
        ROOM_IDS_FIELD_NUMBER: _ClassVar[int]
        room_ids: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, room_ids: _Optional[_Iterable[int]] = ...) -> None: ...
    class DivideRoom(_message.Message):
        __slots__ = ("room_id", "points")
        ROOM_ID_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        room_id: int
        points: _containers.RepeatedCompositeFieldContainer[_common_pb2.Point]
        def __init__(self, room_id: _Optional[int] = ..., points: _Optional[_Iterable[_Union[_common_pb2.Point, _Mapping]]] = ...) -> None: ...
    class RoomsCustom(_message.Message):
        __slots__ = ("custom_enable", "rooms_order", "rooms_parm", "smart_mode_sw", "condition")
        class Condition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            GENERAL: _ClassVar[MapEditRequest.RoomsCustom.Condition]
            RESERVATION_IN_PROGRESS: _ClassVar[MapEditRequest.RoomsCustom.Condition]
        GENERAL: MapEditRequest.RoomsCustom.Condition
        RESERVATION_IN_PROGRESS: MapEditRequest.RoomsCustom.Condition
        class Enable(_message.Message):
            __slots__ = ("value",)
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: bool
            def __init__(self, value: _Optional[bool] = ...) -> None: ...
        class Order(_message.Message):
            __slots__ = ("rooms",)
            class Room(_message.Message):
                __slots__ = ("id", "order")
                ID_FIELD_NUMBER: _ClassVar[int]
                ORDER_FIELD_NUMBER: _ClassVar[int]
                id: int
                order: int
                def __init__(self, id: _Optional[int] = ..., order: _Optional[int] = ...) -> None: ...
            ROOMS_FIELD_NUMBER: _ClassVar[int]
            rooms: _containers.RepeatedCompositeFieldContainer[MapEditRequest.RoomsCustom.Order.Room]
            def __init__(self, rooms: _Optional[_Iterable[_Union[MapEditRequest.RoomsCustom.Order.Room, _Mapping]]] = ...) -> None: ...
        class Parm(_message.Message):
            __slots__ = ("rooms",)
            class Room(_message.Message):
                __slots__ = ("id", "custom")
                class Custom(_message.Message):
                    __slots__ = ("clean_type", "fan", "mop_mode", "clean_extent", "clean_times")
                    CLEAN_TYPE_FIELD_NUMBER: _ClassVar[int]
                    FAN_FIELD_NUMBER: _ClassVar[int]
                    MOP_MODE_FIELD_NUMBER: _ClassVar[int]
                    CLEAN_EXTENT_FIELD_NUMBER: _ClassVar[int]
                    CLEAN_TIMES_FIELD_NUMBER: _ClassVar[int]
                    clean_type: _clean_param_pb2.CleanType
                    fan: _clean_param_pb2.Fan
                    mop_mode: _clean_param_pb2.MopMode
                    clean_extent: _clean_param_pb2.CleanExtent
                    clean_times: int
                    def __init__(self, clean_type: _Optional[_Union[_clean_param_pb2.CleanType, _Mapping]] = ..., fan: _Optional[_Union[_clean_param_pb2.Fan, _Mapping]] = ..., mop_mode: _Optional[_Union[_clean_param_pb2.MopMode, _Mapping]] = ..., clean_extent: _Optional[_Union[_clean_param_pb2.CleanExtent, _Mapping]] = ..., clean_times: _Optional[int] = ...) -> None: ...
                ID_FIELD_NUMBER: _ClassVar[int]
                CUSTOM_FIELD_NUMBER: _ClassVar[int]
                id: int
                custom: MapEditRequest.RoomsCustom.Parm.Room.Custom
                def __init__(self, id: _Optional[int] = ..., custom: _Optional[_Union[MapEditRequest.RoomsCustom.Parm.Room.Custom, _Mapping]] = ...) -> None: ...
            ROOMS_FIELD_NUMBER: _ClassVar[int]
            rooms: _containers.RepeatedCompositeFieldContainer[MapEditRequest.RoomsCustom.Parm.Room]
            def __init__(self, rooms: _Optional[_Iterable[_Union[MapEditRequest.RoomsCustom.Parm.Room, _Mapping]]] = ...) -> None: ...
        CUSTOM_ENABLE_FIELD_NUMBER: _ClassVar[int]
        ROOMS_ORDER_FIELD_NUMBER: _ClassVar[int]
        ROOMS_PARM_FIELD_NUMBER: _ClassVar[int]
        SMART_MODE_SW_FIELD_NUMBER: _ClassVar[int]
        CONDITION_FIELD_NUMBER: _ClassVar[int]
        custom_enable: MapEditRequest.RoomsCustom.Enable
        rooms_order: MapEditRequest.RoomsCustom.Order
        rooms_parm: MapEditRequest.RoomsCustom.Parm
        smart_mode_sw: _common_pb2.Switch
        condition: MapEditRequest.RoomsCustom.Condition
        def __init__(self, custom_enable: _Optional[_Union[MapEditRequest.RoomsCustom.Enable, _Mapping]] = ..., rooms_order: _Optional[_Union[MapEditRequest.RoomsCustom.Order, _Mapping]] = ..., rooms_parm: _Optional[_Union[MapEditRequest.RoomsCustom.Parm, _Mapping]] = ..., smart_mode_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ..., condition: _Optional[_Union[MapEditRequest.RoomsCustom.Condition, str]] = ...) -> None: ...
    class RoomDesc(_message.Message):
        __slots__ = ("id", "name", "floor", "scene")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        FLOOR_FIELD_NUMBER: _ClassVar[int]
        SCENE_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        floor: _common_pb2.Floor
        scene: _common_pb2.RoomScene
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., floor: _Optional[_Union[_common_pb2.Floor, _Mapping]] = ..., scene: _Optional[_Union[_common_pb2.RoomScene, _Mapping]] = ...) -> None: ...
    class CruisePoints(_message.Message):
        __slots__ = ("points",)
        POINTS_FIELD_NUMBER: _ClassVar[int]
        points: _containers.RepeatedCompositeFieldContainer[_common_pb2.Point]
        def __init__(self, points: _Optional[_Iterable[_Union[_common_pb2.Point, _Mapping]]] = ...) -> None: ...
    class Rotation(_message.Message):
        __slots__ = ("angle",)
        ANGLE_FIELD_NUMBER: _ClassVar[int]
        angle: int
        def __init__(self, angle: _Optional[int] = ...) -> None: ...
    class IgnoreObstacle(_message.Message):
        __slots__ = ("valid", "object_type", "photo_id", "point")
        VALID_FIELD_NUMBER: _ClassVar[int]
        OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
        PHOTO_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        valid: bool
        object_type: str
        photo_id: str
        point: _common_pb2.Point
        def __init__(self, valid: _Optional[bool] = ..., object_type: _Optional[str] = ..., photo_id: _Optional[str] = ..., point: _Optional[_Union[_common_pb2.Point, _Mapping]] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    MERGE_ROOMS_FIELD_NUMBER: _ClassVar[int]
    DIVIDE_ROOM_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_ZONE_FIELD_NUMBER: _ClassVar[int]
    ROOM_DESC_FIELD_NUMBER: _ClassVar[int]
    ROOMS_CUSTOM_FIELD_NUMBER: _ClassVar[int]
    CRUISE_POINTS_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    IGNORE_OBSTACLE_FIELD_NUMBER: _ClassVar[int]
    method: MapEditRequest.Method
    seq: int
    map_id: int
    merge_rooms: MapEditRequest.MergeRooms
    divide_room: MapEditRequest.DivideRoom
    restricted_zone: _stream_pb2.RestrictedZone
    room_desc: MapEditRequest.RoomDesc
    rooms_custom: MapEditRequest.RoomsCustom
    cruise_points: MapEditRequest.CruisePoints
    rotation: MapEditRequest.Rotation
    ignore_obstacle: MapEditRequest.IgnoreObstacle
    def __init__(self, method: _Optional[_Union[MapEditRequest.Method, str]] = ..., seq: _Optional[int] = ..., map_id: _Optional[int] = ..., merge_rooms: _Optional[_Union[MapEditRequest.MergeRooms, _Mapping]] = ..., divide_room: _Optional[_Union[MapEditRequest.DivideRoom, _Mapping]] = ..., restricted_zone: _Optional[_Union[_stream_pb2.RestrictedZone, _Mapping]] = ..., room_desc: _Optional[_Union[MapEditRequest.RoomDesc, _Mapping]] = ..., rooms_custom: _Optional[_Union[MapEditRequest.RoomsCustom, _Mapping]] = ..., cruise_points: _Optional[_Union[MapEditRequest.CruisePoints, _Mapping]] = ..., rotation: _Optional[_Union[MapEditRequest.Rotation, _Mapping]] = ..., ignore_obstacle: _Optional[_Union[MapEditRequest.IgnoreObstacle, _Mapping]] = ...) -> None: ...

class MapEditResponse(_message.Message):
    __slots__ = ("method", "seq", "result", "fail_code")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[MapEditResponse.Result]
        STARTED: _ClassVar[MapEditResponse.Result]
        FAILED: _ClassVar[MapEditResponse.Result]
    SUCCESS: MapEditResponse.Result
    STARTED: MapEditResponse.Result
    FAILED: MapEditResponse.Result
    class FailCode(_message.Message):
        __slots__ = ("value",)
        class Value(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            UNKNOWN: _ClassVar[MapEditResponse.FailCode.Value]
            AREA_SMALL: _ClassVar[MapEditResponse.FailCode.Value]
            ROOM_UNADJACENT: _ClassVar[MapEditResponse.FailCode.Value]
            TOO_MANY_ROOMS: _ClassVar[MapEditResponse.FailCode.Value]
        UNKNOWN: MapEditResponse.FailCode.Value
        AREA_SMALL: MapEditResponse.FailCode.Value
        ROOM_UNADJACENT: MapEditResponse.FailCode.Value
        TOO_MANY_ROOMS: MapEditResponse.FailCode.Value
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: MapEditResponse.FailCode.Value
        def __init__(self, value: _Optional[_Union[MapEditResponse.FailCode.Value, str]] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    FAIL_CODE_FIELD_NUMBER: _ClassVar[int]
    method: MapEditRequest.Method
    seq: int
    result: MapEditResponse.Result
    fail_code: MapEditResponse.FailCode
    def __init__(self, method: _Optional[_Union[MapEditRequest.Method, str]] = ..., seq: _Optional[int] = ..., result: _Optional[_Union[MapEditResponse.Result, str]] = ..., fail_code: _Optional[_Union[MapEditResponse.FailCode, _Mapping]] = ...) -> None: ...
