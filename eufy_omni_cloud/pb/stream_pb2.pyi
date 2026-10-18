from . import common_pb2 as _common_pb2
from . import clean_param_pb2 as _clean_param_pb2
from . import control_pb2 as _control_pb2
from . import scene_pb2 as _scene_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Metadata(_message.Message):
    __slots__ = ("versions", "chan_ids")
    class Versions(_message.Message):
        __slots__ = ("map_data",)
        MAP_DATA_FIELD_NUMBER: _ClassVar[int]
        map_data: int
        def __init__(self, map_data: _Optional[int] = ...) -> None: ...
    class ChanIds(_message.Message):
        __slots__ = ("map_info", "path", "room_outline", "room_params", "restricted_zone", "dynamic_data", "temporary_data", "obstacle_info", "map_data", "cruise_data")
        MAP_INFO_FIELD_NUMBER: _ClassVar[int]
        PATH_FIELD_NUMBER: _ClassVar[int]
        ROOM_OUTLINE_FIELD_NUMBER: _ClassVar[int]
        ROOM_PARAMS_FIELD_NUMBER: _ClassVar[int]
        RESTRICTED_ZONE_FIELD_NUMBER: _ClassVar[int]
        DYNAMIC_DATA_FIELD_NUMBER: _ClassVar[int]
        TEMPORARY_DATA_FIELD_NUMBER: _ClassVar[int]
        OBSTACLE_INFO_FIELD_NUMBER: _ClassVar[int]
        MAP_DATA_FIELD_NUMBER: _ClassVar[int]
        CRUISE_DATA_FIELD_NUMBER: _ClassVar[int]
        map_info: int
        path: int
        room_outline: int
        room_params: int
        restricted_zone: int
        dynamic_data: int
        temporary_data: int
        obstacle_info: int
        map_data: int
        cruise_data: int
        def __init__(self, map_info: _Optional[int] = ..., path: _Optional[int] = ..., room_outline: _Optional[int] = ..., room_params: _Optional[int] = ..., restricted_zone: _Optional[int] = ..., dynamic_data: _Optional[int] = ..., temporary_data: _Optional[int] = ..., obstacle_info: _Optional[int] = ..., map_data: _Optional[int] = ..., cruise_data: _Optional[int] = ...) -> None: ...
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    CHAN_IDS_FIELD_NUMBER: _ClassVar[int]
    versions: Metadata.Versions
    chan_ids: Metadata.ChanIds
    def __init__(self, versions: _Optional[_Union[Metadata.Versions, _Mapping]] = ..., chan_ids: _Optional[_Union[Metadata.ChanIds, _Mapping]] = ...) -> None: ...

class MapInfo(_message.Message):
    __slots__ = ("map_id", "width", "height", "resolution", "origin", "docks", "type", "seq", "angle", "docks_v2")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INCOMPLETE: _ClassVar[MapInfo.Type]
        ROUGH: _ClassVar[MapInfo.Type]
        EFFECTIVE: _ClassVar[MapInfo.Type]
        LIST_FULL: _ClassVar[MapInfo.Type]
    INCOMPLETE: MapInfo.Type
    ROUGH: MapInfo.Type
    EFFECTIVE: MapInfo.Type
    LIST_FULL: MapInfo.Type
    class Dock(_message.Message):
        __slots__ = ("type", "pose")
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            ADAPTER: _ClassVar[MapInfo.Dock.Type]
            STATION: _ClassVar[MapInfo.Dock.Type]
        ADAPTER: MapInfo.Dock.Type
        STATION: MapInfo.Dock.Type
        TYPE_FIELD_NUMBER: _ClassVar[int]
        POSE_FIELD_NUMBER: _ClassVar[int]
        type: MapInfo.Dock.Type
        pose: _common_pb2.Pose
        def __init__(self, type: _Optional[_Union[MapInfo.Dock.Type, str]] = ..., pose: _Optional[_Union[_common_pb2.Pose, _Mapping]] = ...) -> None: ...
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    DOCKS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    DOCKS_V2_FIELD_NUMBER: _ClassVar[int]
    map_id: int
    width: int
    height: int
    resolution: int
    origin: _common_pb2.Point
    docks: _containers.RepeatedCompositeFieldContainer[_common_pb2.Pose]
    type: MapInfo.Type
    seq: int
    angle: int
    docks_v2: _containers.RepeatedCompositeFieldContainer[MapInfo.Dock]
    def __init__(self, map_id: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., resolution: _Optional[int] = ..., origin: _Optional[_Union[_common_pb2.Point, _Mapping]] = ..., docks: _Optional[_Iterable[_Union[_common_pb2.Pose, _Mapping]]] = ..., type: _Optional[_Union[MapInfo.Type, str]] = ..., seq: _Optional[int] = ..., angle: _Optional[int] = ..., docks_v2: _Optional[_Iterable[_Union[MapInfo.Dock, _Mapping]]] = ...) -> None: ...

class Map(_message.Message):
    __slots__ = ("map_id", "seq", "frame", "pixels", "pixel_size", "info", "name", "id", "releases", "index")
    class Frame(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        I: _ClassVar[Map.Frame]
        P: _ClassVar[Map.Frame]
    I: Map.Frame
    P: Map.Frame
    class PixelValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOW: _ClassVar[Map.PixelValue]
        OBSTACLE: _ClassVar[Map.PixelValue]
        FREE: _ClassVar[Map.PixelValue]
        CARPET: _ClassVar[Map.PixelValue]
    UNKNOW: Map.PixelValue
    OBSTACLE: Map.PixelValue
    FREE: Map.PixelValue
    CARPET: Map.PixelValue
    class Index(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: int
        def __init__(self, value: _Optional[int] = ...) -> None: ...
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    PIXEL_SIZE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    map_id: int
    seq: int
    frame: Map.Frame
    pixels: bytes
    pixel_size: int
    info: MapInfo
    name: str
    id: int
    releases: int
    index: Map.Index
    def __init__(self, map_id: _Optional[int] = ..., seq: _Optional[int] = ..., frame: _Optional[_Union[Map.Frame, str]] = ..., pixels: _Optional[bytes] = ..., pixel_size: _Optional[int] = ..., info: _Optional[_Union[MapInfo, _Mapping]] = ..., name: _Optional[str] = ..., id: _Optional[int] = ..., releases: _Optional[int] = ..., index: _Optional[_Union[Map.Index, _Mapping]] = ...) -> None: ...

class PathPoint(_message.Message):
    __slots__ = ("xy", "flags")
    XY_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    xy: int
    flags: int
    def __init__(self, xy: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...

class RoomOutline(_message.Message):
    __slots__ = ("map_id", "releases", "width", "height", "resolution", "origin", "pixels", "pixel_size")
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    PIXEL_SIZE_FIELD_NUMBER: _ClassVar[int]
    map_id: int
    releases: int
    width: int
    height: int
    resolution: int
    origin: _common_pb2.Point
    pixels: bytes
    pixel_size: int
    def __init__(self, map_id: _Optional[int] = ..., releases: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., resolution: _Optional[int] = ..., origin: _Optional[_Union[_common_pb2.Point, _Mapping]] = ..., pixels: _Optional[bytes] = ..., pixel_size: _Optional[int] = ...) -> None: ...

class RoomParams(_message.Message):
    __slots__ = ("custom_enable", "rooms", "map_id", "releases", "smart_mode_sw")
    class Room(_message.Message):
        __slots__ = ("id", "name", "floor", "scene", "order", "custom")
        class Order(_message.Message):
            __slots__ = ("value",)
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: int
            def __init__(self, value: _Optional[int] = ...) -> None: ...
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
        NAME_FIELD_NUMBER: _ClassVar[int]
        FLOOR_FIELD_NUMBER: _ClassVar[int]
        SCENE_FIELD_NUMBER: _ClassVar[int]
        ORDER_FIELD_NUMBER: _ClassVar[int]
        CUSTOM_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        floor: _common_pb2.Floor
        scene: _common_pb2.RoomScene
        order: RoomParams.Room.Order
        custom: RoomParams.Room.Custom
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., floor: _Optional[_Union[_common_pb2.Floor, _Mapping]] = ..., scene: _Optional[_Union[_common_pb2.RoomScene, _Mapping]] = ..., order: _Optional[_Union[RoomParams.Room.Order, _Mapping]] = ..., custom: _Optional[_Union[RoomParams.Room.Custom, _Mapping]] = ...) -> None: ...
    CUSTOM_ENABLE_FIELD_NUMBER: _ClassVar[int]
    ROOMS_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    SMART_MODE_SW_FIELD_NUMBER: _ClassVar[int]
    custom_enable: bool
    rooms: _containers.RepeatedCompositeFieldContainer[RoomParams.Room]
    map_id: int
    releases: int
    smart_mode_sw: _common_pb2.Switch
    def __init__(self, custom_enable: _Optional[bool] = ..., rooms: _Optional[_Iterable[_Union[RoomParams.Room, _Mapping]]] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ..., smart_mode_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ...) -> None: ...

class RestrictedZone(_message.Message):
    __slots__ = ("virtual_walls", "forbidden_zones", "ban_mop_zones", "map_id", "releases", "suggestion")
    class Suggestion(_message.Message):
        __slots__ = ("virtual_walls", "forbidden_zones", "ban_mop_zones")
        class LineWrap(_message.Message):
            __slots__ = ("id", "line")
            ID_FIELD_NUMBER: _ClassVar[int]
            LINE_FIELD_NUMBER: _ClassVar[int]
            id: int
            line: _common_pb2.Line
            def __init__(self, id: _Optional[int] = ..., line: _Optional[_Union[_common_pb2.Line, _Mapping]] = ...) -> None: ...
        class QuadrangleWrap(_message.Message):
            __slots__ = ("id", "quadrangle")
            ID_FIELD_NUMBER: _ClassVar[int]
            QUADRANGLE_FIELD_NUMBER: _ClassVar[int]
            id: int
            quadrangle: _common_pb2.Quadrangle
            def __init__(self, id: _Optional[int] = ..., quadrangle: _Optional[_Union[_common_pb2.Quadrangle, _Mapping]] = ...) -> None: ...
        VIRTUAL_WALLS_FIELD_NUMBER: _ClassVar[int]
        FORBIDDEN_ZONES_FIELD_NUMBER: _ClassVar[int]
        BAN_MOP_ZONES_FIELD_NUMBER: _ClassVar[int]
        virtual_walls: _containers.RepeatedCompositeFieldContainer[RestrictedZone.Suggestion.LineWrap]
        forbidden_zones: _containers.RepeatedCompositeFieldContainer[RestrictedZone.Suggestion.QuadrangleWrap]
        ban_mop_zones: _containers.RepeatedCompositeFieldContainer[RestrictedZone.Suggestion.QuadrangleWrap]
        def __init__(self, virtual_walls: _Optional[_Iterable[_Union[RestrictedZone.Suggestion.LineWrap, _Mapping]]] = ..., forbidden_zones: _Optional[_Iterable[_Union[RestrictedZone.Suggestion.QuadrangleWrap, _Mapping]]] = ..., ban_mop_zones: _Optional[_Iterable[_Union[RestrictedZone.Suggestion.QuadrangleWrap, _Mapping]]] = ...) -> None: ...
    VIRTUAL_WALLS_FIELD_NUMBER: _ClassVar[int]
    FORBIDDEN_ZONES_FIELD_NUMBER: _ClassVar[int]
    BAN_MOP_ZONES_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    SUGGESTION_FIELD_NUMBER: _ClassVar[int]
    virtual_walls: _containers.RepeatedCompositeFieldContainer[_common_pb2.Line]
    forbidden_zones: _containers.RepeatedCompositeFieldContainer[_common_pb2.Quadrangle]
    ban_mop_zones: _containers.RepeatedCompositeFieldContainer[_common_pb2.Quadrangle]
    map_id: int
    releases: int
    suggestion: RestrictedZone.Suggestion
    def __init__(self, virtual_walls: _Optional[_Iterable[_Union[_common_pb2.Line, _Mapping]]] = ..., forbidden_zones: _Optional[_Iterable[_Union[_common_pb2.Quadrangle, _Mapping]]] = ..., ban_mop_zones: _Optional[_Iterable[_Union[_common_pb2.Quadrangle, _Mapping]]] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ..., suggestion: _Optional[_Union[RestrictedZone.Suggestion, _Mapping]] = ...) -> None: ...

class DynamicData(_message.Message):
    __slots__ = ("cur_pose",)
    CUR_POSE_FIELD_NUMBER: _ClassVar[int]
    cur_pose: _common_pb2.Pose
    def __init__(self, cur_pose: _Optional[_Union[_common_pb2.Pose, _Mapping]] = ...) -> None: ...

class TemporaryData(_message.Message):
    __slots__ = ("select_rooms_clean", "select_zones_clean", "goto_location", "select_point_cruise", "select_zones_cruise")
    SELECT_ROOMS_CLEAN_FIELD_NUMBER: _ClassVar[int]
    SELECT_ZONES_CLEAN_FIELD_NUMBER: _ClassVar[int]
    GOTO_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SELECT_POINT_CRUISE_FIELD_NUMBER: _ClassVar[int]
    SELECT_ZONES_CRUISE_FIELD_NUMBER: _ClassVar[int]
    select_rooms_clean: _control_pb2.SelectRoomsClean
    select_zones_clean: _control_pb2.SelectZonesClean
    goto_location: _control_pb2.Goto
    select_point_cruise: _control_pb2.PointCruise
    select_zones_cruise: _control_pb2.ZonesCruise
    def __init__(self, select_rooms_clean: _Optional[_Union[_control_pb2.SelectRoomsClean, _Mapping]] = ..., select_zones_clean: _Optional[_Union[_control_pb2.SelectZonesClean, _Mapping]] = ..., goto_location: _Optional[_Union[_control_pb2.Goto, _Mapping]] = ..., select_point_cruise: _Optional[_Union[_control_pb2.PointCruise, _Mapping]] = ..., select_zones_cruise: _Optional[_Union[_control_pb2.ZonesCruise, _Mapping]] = ...) -> None: ...

class ObstacleInfo(_message.Message):
    __slots__ = ("map_id", "releases", "obstacles")
    class Obstacle(_message.Message):
        __slots__ = ("object_type", "show_type", "show_points", "bitmap", "theta", "photo_id", "accuracy", "valid")
        class ShowType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            POSITION: _ClassVar[ObstacleInfo.Obstacle.ShowType]
            OUTLINE: _ClassVar[ObstacleInfo.Obstacle.ShowType]
            FILL: _ClassVar[ObstacleInfo.Obstacle.ShowType]
            BITMAP: _ClassVar[ObstacleInfo.Obstacle.ShowType]
        POSITION: ObstacleInfo.Obstacle.ShowType
        OUTLINE: ObstacleInfo.Obstacle.ShowType
        FILL: ObstacleInfo.Obstacle.ShowType
        BITMAP: ObstacleInfo.Obstacle.ShowType
        class Bitmap(_message.Message):
            __slots__ = ("ref_point", "width", "height", "data_len", "data")
            REF_POINT_FIELD_NUMBER: _ClassVar[int]
            WIDTH_FIELD_NUMBER: _ClassVar[int]
            HEIGHT_FIELD_NUMBER: _ClassVar[int]
            DATA_LEN_FIELD_NUMBER: _ClassVar[int]
            DATA_FIELD_NUMBER: _ClassVar[int]
            ref_point: _common_pb2.Point
            width: int
            height: int
            data_len: int
            data: bytes
            def __init__(self, ref_point: _Optional[_Union[_common_pb2.Point, _Mapping]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., data_len: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...
        class Valid(_message.Message):
            __slots__ = ("value",)
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: bool
            def __init__(self, value: _Optional[bool] = ...) -> None: ...
        OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
        SHOW_TYPE_FIELD_NUMBER: _ClassVar[int]
        SHOW_POINTS_FIELD_NUMBER: _ClassVar[int]
        BITMAP_FIELD_NUMBER: _ClassVar[int]
        THETA_FIELD_NUMBER: _ClassVar[int]
        PHOTO_ID_FIELD_NUMBER: _ClassVar[int]
        ACCURACY_FIELD_NUMBER: _ClassVar[int]
        VALID_FIELD_NUMBER: _ClassVar[int]
        object_type: str
        show_type: ObstacleInfo.Obstacle.ShowType
        show_points: _containers.RepeatedCompositeFieldContainer[_common_pb2.Point]
        bitmap: ObstacleInfo.Obstacle.Bitmap
        theta: int
        photo_id: str
        accuracy: int
        valid: ObstacleInfo.Obstacle.Valid
        def __init__(self, object_type: _Optional[str] = ..., show_type: _Optional[_Union[ObstacleInfo.Obstacle.ShowType, str]] = ..., show_points: _Optional[_Iterable[_Union[_common_pb2.Point, _Mapping]]] = ..., bitmap: _Optional[_Union[ObstacleInfo.Obstacle.Bitmap, _Mapping]] = ..., theta: _Optional[int] = ..., photo_id: _Optional[str] = ..., accuracy: _Optional[int] = ..., valid: _Optional[_Union[ObstacleInfo.Obstacle.Valid, _Mapping]] = ...) -> None: ...
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    OBSTACLES_FIELD_NUMBER: _ClassVar[int]
    map_id: int
    releases: int
    obstacles: _containers.RepeatedCompositeFieldContainer[ObstacleInfo.Obstacle]
    def __init__(self, map_id: _Optional[int] = ..., releases: _Optional[int] = ..., obstacles: _Optional[_Iterable[_Union[ObstacleInfo.Obstacle, _Mapping]]] = ...) -> None: ...

class CruiseData(_message.Message):
    __slots__ = ("cruise_data", "map_id", "releases")
    class ProcessData(_message.Message):
        __slots__ = ("points", "photo_id")
        POINTS_FIELD_NUMBER: _ClassVar[int]
        PHOTO_ID_FIELD_NUMBER: _ClassVar[int]
        points: _common_pb2.Point
        photo_id: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, points: _Optional[_Union[_common_pb2.Point, _Mapping]] = ..., photo_id: _Optional[_Iterable[str]] = ...) -> None: ...
    CRUISE_DATA_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    cruise_data: _containers.RepeatedCompositeFieldContainer[CruiseData.ProcessData]
    map_id: int
    releases: int
    def __init__(self, cruise_data: _Optional[_Iterable[_Union[CruiseData.ProcessData, _Mapping]]] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ...) -> None: ...

class MapDescription(_message.Message):
    __slots__ = ("name", "create_cause", "create_time", "last_time", "map_id", "releases")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATE_CAUSE_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_TIME_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    name: str
    create_cause: int
    create_time: int
    last_time: int
    map_id: int
    releases: int
    def __init__(self, name: _Optional[str] = ..., create_cause: _Optional[int] = ..., create_time: _Optional[int] = ..., last_time: _Optional[int] = ..., map_id: _Optional[int] = ..., releases: _Optional[int] = ...) -> None: ...

class MapBackup(_message.Message):
    __slots__ = ("desc", "map", "rooms", "room_params", "restricted_zone")
    DESC_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    ROOMS_FIELD_NUMBER: _ClassVar[int]
    ROOM_PARAMS_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_ZONE_FIELD_NUMBER: _ClassVar[int]
    desc: MapDescription
    map: Map
    rooms: RoomOutline
    room_params: RoomParams
    restricted_zone: RestrictedZone
    def __init__(self, desc: _Optional[_Union[MapDescription, _Mapping]] = ..., map: _Optional[_Union[Map, _Mapping]] = ..., rooms: _Optional[_Union[RoomOutline, _Mapping]] = ..., room_params: _Optional[_Union[RoomParams, _Mapping]] = ..., restricted_zone: _Optional[_Union[RestrictedZone, _Mapping]] = ...) -> None: ...

class SceneWrap(_message.Message):
    __slots__ = ("scenes",)
    class Scene(_message.Message):
        __slots__ = ("info", "tasks")
        INFO_FIELD_NUMBER: _ClassVar[int]
        TASKS_FIELD_NUMBER: _ClassVar[int]
        info: _scene_pb2.SceneInfo
        tasks: _containers.RepeatedCompositeFieldContainer[_scene_pb2.SceneTask]
        def __init__(self, info: _Optional[_Union[_scene_pb2.SceneInfo, _Mapping]] = ..., tasks: _Optional[_Iterable[_Union[_scene_pb2.SceneTask, _Mapping]]] = ...) -> None: ...
    SCENES_FIELD_NUMBER: _ClassVar[int]
    scenes: _containers.RepeatedCompositeFieldContainer[SceneWrap.Scene]
    def __init__(self, scenes: _Optional[_Iterable[_Union[SceneWrap.Scene, _Mapping]]] = ...) -> None: ...
