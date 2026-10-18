from . import common_pb2 as _common_pb2
from . import clean_param_pb2 as _clean_param_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimerInfo(_message.Message):
    __slots__ = ("id", "status", "desc", "addition", "action")
    class Id(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: int
        def __init__(self, value: _Optional[int] = ...) -> None: ...
    class Status(_message.Message):
        __slots__ = ("valid", "opened")
        VALID_FIELD_NUMBER: _ClassVar[int]
        OPENED_FIELD_NUMBER: _ClassVar[int]
        valid: bool
        opened: bool
        def __init__(self, valid: _Optional[bool] = ..., opened: _Optional[bool] = ...) -> None: ...
    class Desc(_message.Message):
        __slots__ = ("trigger", "timing", "cycle")
        class Trigger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SINGLE: _ClassVar[TimerInfo.Desc.Trigger]
            CYCLE: _ClassVar[TimerInfo.Desc.Trigger]
        SINGLE: TimerInfo.Desc.Trigger
        CYCLE: TimerInfo.Desc.Trigger
        class Timing(_message.Message):
            __slots__ = ("user_tz", "summer", "hours", "minutes")
            USER_TZ_FIELD_NUMBER: _ClassVar[int]
            SUMMER_FIELD_NUMBER: _ClassVar[int]
            HOURS_FIELD_NUMBER: _ClassVar[int]
            MINUTES_FIELD_NUMBER: _ClassVar[int]
            user_tz: int
            summer: bool
            hours: int
            minutes: int
            def __init__(self, user_tz: _Optional[int] = ..., summer: _Optional[bool] = ..., hours: _Optional[int] = ..., minutes: _Optional[int] = ...) -> None: ...
        class Cycle(_message.Message):
            __slots__ = ("week_bits",)
            WEEK_BITS_FIELD_NUMBER: _ClassVar[int]
            week_bits: int
            def __init__(self, week_bits: _Optional[int] = ...) -> None: ...
        TRIGGER_FIELD_NUMBER: _ClassVar[int]
        TIMING_FIELD_NUMBER: _ClassVar[int]
        CYCLE_FIELD_NUMBER: _ClassVar[int]
        trigger: TimerInfo.Desc.Trigger
        timing: TimerInfo.Desc.Timing
        cycle: TimerInfo.Desc.Cycle
        def __init__(self, trigger: _Optional[_Union[TimerInfo.Desc.Trigger, str]] = ..., timing: _Optional[_Union[TimerInfo.Desc.Timing, _Mapping]] = ..., cycle: _Optional[_Union[TimerInfo.Desc.Cycle, _Mapping]] = ...) -> None: ...
    class Addition(_message.Message):
        __slots__ = ("create_time", "create_user_id", "renew_time", "renew_user_id")
        CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        CREATE_USER_ID_FIELD_NUMBER: _ClassVar[int]
        RENEW_TIME_FIELD_NUMBER: _ClassVar[int]
        RENEW_USER_ID_FIELD_NUMBER: _ClassVar[int]
        create_time: int
        create_user_id: str
        renew_time: int
        renew_user_id: str
        def __init__(self, create_time: _Optional[int] = ..., create_user_id: _Optional[str] = ..., renew_time: _Optional[int] = ..., renew_user_id: _Optional[str] = ...) -> None: ...
    class Action(_message.Message):
        __slots__ = ("type", "precondition", "sche_auto_clean", "sche_rooms_clean", "sche_cruise", "sche_scene_clean")
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SCHEDULE_AUTO_CLEAN: _ClassVar[TimerInfo.Action.Type]
            SCHEDULE_ROOMS_CLEAN: _ClassVar[TimerInfo.Action.Type]
            SCHEDULE_CRUISE: _ClassVar[TimerInfo.Action.Type]
            SCHEDULE_SCENE_CLEAN: _ClassVar[TimerInfo.Action.Type]
        SCHEDULE_AUTO_CLEAN: TimerInfo.Action.Type
        SCHEDULE_ROOMS_CLEAN: TimerInfo.Action.Type
        SCHEDULE_CRUISE: TimerInfo.Action.Type
        SCHEDULE_SCENE_CLEAN: TimerInfo.Action.Type
        class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            GENERAL: _ClassVar[TimerInfo.Action.Mode]
            CUSTOMIZE: _ClassVar[TimerInfo.Action.Mode]
        GENERAL: TimerInfo.Action.Mode
        CUSTOMIZE: TimerInfo.Action.Mode
        class Precondition(_message.Message):
            __slots__ = ()
            def __init__(self) -> None: ...
        class ScheduleAutoClean(_message.Message):
            __slots__ = ("mode", "general")
            class General(_message.Message):
                __slots__ = ("fan", "mop_mode", "clean_type", "clean_extent", "smart_mode_sw")
                FAN_FIELD_NUMBER: _ClassVar[int]
                MOP_MODE_FIELD_NUMBER: _ClassVar[int]
                CLEAN_TYPE_FIELD_NUMBER: _ClassVar[int]
                CLEAN_EXTENT_FIELD_NUMBER: _ClassVar[int]
                SMART_MODE_SW_FIELD_NUMBER: _ClassVar[int]
                fan: _clean_param_pb2.Fan
                mop_mode: _clean_param_pb2.MopMode
                clean_type: _clean_param_pb2.CleanType
                clean_extent: _clean_param_pb2.CleanExtent
                smart_mode_sw: _common_pb2.Switch
                def __init__(self, fan: _Optional[_Union[_clean_param_pb2.Fan, _Mapping]] = ..., mop_mode: _Optional[_Union[_clean_param_pb2.MopMode, _Mapping]] = ..., clean_type: _Optional[_Union[_clean_param_pb2.CleanType, _Mapping]] = ..., clean_extent: _Optional[_Union[_clean_param_pb2.CleanExtent, _Mapping]] = ..., smart_mode_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ...) -> None: ...
            MODE_FIELD_NUMBER: _ClassVar[int]
            GENERAL_FIELD_NUMBER: _ClassVar[int]
            mode: TimerInfo.Action.Mode
            general: TimerInfo.Action.ScheduleAutoClean.General
            def __init__(self, mode: _Optional[_Union[TimerInfo.Action.Mode, str]] = ..., general: _Optional[_Union[TimerInfo.Action.ScheduleAutoClean.General, _Mapping]] = ...) -> None: ...
        class ScheduleRoomsClean(_message.Message):
            __slots__ = ("mode", "general", "custom")
            class General(_message.Message):
                __slots__ = ("map_id", "fan", "mop_mode", "clean_type", "clean_extent", "rooms")
                class Room(_message.Message):
                    __slots__ = ("id", "order")
                    ID_FIELD_NUMBER: _ClassVar[int]
                    ORDER_FIELD_NUMBER: _ClassVar[int]
                    id: int
                    order: int
                    def __init__(self, id: _Optional[int] = ..., order: _Optional[int] = ...) -> None: ...
                MAP_ID_FIELD_NUMBER: _ClassVar[int]
                FAN_FIELD_NUMBER: _ClassVar[int]
                MOP_MODE_FIELD_NUMBER: _ClassVar[int]
                CLEAN_TYPE_FIELD_NUMBER: _ClassVar[int]
                CLEAN_EXTENT_FIELD_NUMBER: _ClassVar[int]
                ROOMS_FIELD_NUMBER: _ClassVar[int]
                map_id: int
                fan: _clean_param_pb2.Fan
                mop_mode: _clean_param_pb2.MopMode
                clean_type: _clean_param_pb2.CleanType
                clean_extent: _clean_param_pb2.CleanExtent
                rooms: _containers.RepeatedCompositeFieldContainer[TimerInfo.Action.ScheduleRoomsClean.General.Room]
                def __init__(self, map_id: _Optional[int] = ..., fan: _Optional[_Union[_clean_param_pb2.Fan, _Mapping]] = ..., mop_mode: _Optional[_Union[_clean_param_pb2.MopMode, _Mapping]] = ..., clean_type: _Optional[_Union[_clean_param_pb2.CleanType, _Mapping]] = ..., clean_extent: _Optional[_Union[_clean_param_pb2.CleanExtent, _Mapping]] = ..., rooms: _Optional[_Iterable[_Union[TimerInfo.Action.ScheduleRoomsClean.General.Room, _Mapping]]] = ...) -> None: ...
            class Custom(_message.Message):
                __slots__ = ("map_id", "smart_mode_sw", "rooms")
                class Room(_message.Message):
                    __slots__ = ("id", "order", "clean_type", "fan", "mop_mode", "clean_extent", "clean_times")
                    ID_FIELD_NUMBER: _ClassVar[int]
                    ORDER_FIELD_NUMBER: _ClassVar[int]
                    CLEAN_TYPE_FIELD_NUMBER: _ClassVar[int]
                    FAN_FIELD_NUMBER: _ClassVar[int]
                    MOP_MODE_FIELD_NUMBER: _ClassVar[int]
                    CLEAN_EXTENT_FIELD_NUMBER: _ClassVar[int]
                    CLEAN_TIMES_FIELD_NUMBER: _ClassVar[int]
                    id: int
                    order: int
                    clean_type: _clean_param_pb2.CleanType
                    fan: _clean_param_pb2.Fan
                    mop_mode: _clean_param_pb2.MopMode
                    clean_extent: _clean_param_pb2.CleanExtent
                    clean_times: int
                    def __init__(self, id: _Optional[int] = ..., order: _Optional[int] = ..., clean_type: _Optional[_Union[_clean_param_pb2.CleanType, _Mapping]] = ..., fan: _Optional[_Union[_clean_param_pb2.Fan, _Mapping]] = ..., mop_mode: _Optional[_Union[_clean_param_pb2.MopMode, _Mapping]] = ..., clean_extent: _Optional[_Union[_clean_param_pb2.CleanExtent, _Mapping]] = ..., clean_times: _Optional[int] = ...) -> None: ...
                MAP_ID_FIELD_NUMBER: _ClassVar[int]
                SMART_MODE_SW_FIELD_NUMBER: _ClassVar[int]
                ROOMS_FIELD_NUMBER: _ClassVar[int]
                map_id: int
                smart_mode_sw: _common_pb2.Switch
                rooms: _containers.RepeatedCompositeFieldContainer[TimerInfo.Action.ScheduleRoomsClean.Custom.Room]
                def __init__(self, map_id: _Optional[int] = ..., smart_mode_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ..., rooms: _Optional[_Iterable[_Union[TimerInfo.Action.ScheduleRoomsClean.Custom.Room, _Mapping]]] = ...) -> None: ...
            MODE_FIELD_NUMBER: _ClassVar[int]
            GENERAL_FIELD_NUMBER: _ClassVar[int]
            CUSTOM_FIELD_NUMBER: _ClassVar[int]
            mode: TimerInfo.Action.Mode
            general: TimerInfo.Action.ScheduleRoomsClean.General
            custom: TimerInfo.Action.ScheduleRoomsClean.Custom
            def __init__(self, mode: _Optional[_Union[TimerInfo.Action.Mode, str]] = ..., general: _Optional[_Union[TimerInfo.Action.ScheduleRoomsClean.General, _Mapping]] = ..., custom: _Optional[_Union[TimerInfo.Action.ScheduleRoomsClean.Custom, _Mapping]] = ...) -> None: ...
        class ScheduleCruise(_message.Message):
            __slots__ = ("map_id",)
            MAP_ID_FIELD_NUMBER: _ClassVar[int]
            map_id: int
            def __init__(self, map_id: _Optional[int] = ...) -> None: ...
        class ScheduleSceneClean(_message.Message):
            __slots__ = ("scene_id", "scene_name")
            SCENE_ID_FIELD_NUMBER: _ClassVar[int]
            SCENE_NAME_FIELD_NUMBER: _ClassVar[int]
            scene_id: int
            scene_name: str
            def __init__(self, scene_id: _Optional[int] = ..., scene_name: _Optional[str] = ...) -> None: ...
        TYPE_FIELD_NUMBER: _ClassVar[int]
        PRECONDITION_FIELD_NUMBER: _ClassVar[int]
        SCHE_AUTO_CLEAN_FIELD_NUMBER: _ClassVar[int]
        SCHE_ROOMS_CLEAN_FIELD_NUMBER: _ClassVar[int]
        SCHE_CRUISE_FIELD_NUMBER: _ClassVar[int]
        SCHE_SCENE_CLEAN_FIELD_NUMBER: _ClassVar[int]
        type: TimerInfo.Action.Type
        precondition: TimerInfo.Action.Precondition
        sche_auto_clean: TimerInfo.Action.ScheduleAutoClean
        sche_rooms_clean: TimerInfo.Action.ScheduleRoomsClean
        sche_cruise: TimerInfo.Action.ScheduleCruise
        sche_scene_clean: TimerInfo.Action.ScheduleSceneClean
        def __init__(self, type: _Optional[_Union[TimerInfo.Action.Type, str]] = ..., precondition: _Optional[_Union[TimerInfo.Action.Precondition, _Mapping]] = ..., sche_auto_clean: _Optional[_Union[TimerInfo.Action.ScheduleAutoClean, _Mapping]] = ..., sche_rooms_clean: _Optional[_Union[TimerInfo.Action.ScheduleRoomsClean, _Mapping]] = ..., sche_cruise: _Optional[_Union[TimerInfo.Action.ScheduleCruise, _Mapping]] = ..., sche_scene_clean: _Optional[_Union[TimerInfo.Action.ScheduleSceneClean, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    ADDITION_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    id: TimerInfo.Id
    status: TimerInfo.Status
    desc: TimerInfo.Desc
    addition: TimerInfo.Addition
    action: TimerInfo.Action
    def __init__(self, id: _Optional[_Union[TimerInfo.Id, _Mapping]] = ..., status: _Optional[_Union[TimerInfo.Status, _Mapping]] = ..., desc: _Optional[_Union[TimerInfo.Desc, _Mapping]] = ..., addition: _Optional[_Union[TimerInfo.Addition, _Mapping]] = ..., action: _Optional[_Union[TimerInfo.Action, _Mapping]] = ...) -> None: ...

class TimerRequest(_message.Message):
    __slots__ = ("method", "seq", "timer")
    class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFAULT: _ClassVar[TimerRequest.Method]
        ADD: _ClassVar[TimerRequest.Method]
        DELETE: _ClassVar[TimerRequest.Method]
        MOTIFY: _ClassVar[TimerRequest.Method]
        OPEN: _ClassVar[TimerRequest.Method]
        CLOSE: _ClassVar[TimerRequest.Method]
        INQUIRY: _ClassVar[TimerRequest.Method]
        IGNORE_ONCE: _ClassVar[TimerRequest.Method]
    DEFAULT: TimerRequest.Method
    ADD: TimerRequest.Method
    DELETE: TimerRequest.Method
    MOTIFY: TimerRequest.Method
    OPEN: TimerRequest.Method
    CLOSE: TimerRequest.Method
    INQUIRY: TimerRequest.Method
    IGNORE_ONCE: TimerRequest.Method
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    TIMER_FIELD_NUMBER: _ClassVar[int]
    method: TimerRequest.Method
    seq: int
    timer: TimerInfo
    def __init__(self, method: _Optional[_Union[TimerRequest.Method, str]] = ..., seq: _Optional[int] = ..., timer: _Optional[_Union[TimerInfo, _Mapping]] = ...) -> None: ...

class TimerResponse(_message.Message):
    __slots__ = ("method", "seq", "result", "timers")
    class Result(_message.Message):
        __slots__ = ("value", "err_code")
        class Value(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SUCCESS: _ClassVar[TimerResponse.Result.Value]
            FAILED: _ClassVar[TimerResponse.Result.Value]
        SUCCESS: TimerResponse.Result.Value
        FAILED: TimerResponse.Result.Value
        VALUE_FIELD_NUMBER: _ClassVar[int]
        ERR_CODE_FIELD_NUMBER: _ClassVar[int]
        value: TimerResponse.Result.Value
        err_code: int
        def __init__(self, value: _Optional[_Union[TimerResponse.Result.Value, str]] = ..., err_code: _Optional[int] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TIMERS_FIELD_NUMBER: _ClassVar[int]
    method: TimerRequest.Method
    seq: int
    result: TimerResponse.Result
    timers: _containers.RepeatedCompositeFieldContainer[TimerInfo]
    def __init__(self, method: _Optional[_Union[TimerRequest.Method, str]] = ..., seq: _Optional[int] = ..., result: _Optional[_Union[TimerResponse.Result, _Mapping]] = ..., timers: _Optional[_Iterable[_Union[TimerInfo, _Mapping]]] = ...) -> None: ...
