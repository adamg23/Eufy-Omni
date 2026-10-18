from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorSetting(_message.Message):
    __slots__ = ("warn_mask", "obstacle_reminder_mask")
    WARN_MASK_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_REMINDER_MASK_FIELD_NUMBER: _ClassVar[int]
    warn_mask: _containers.RepeatedScalarFieldContainer[int]
    obstacle_reminder_mask: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, warn_mask: _Optional[_Iterable[int]] = ..., obstacle_reminder_mask: _Optional[_Iterable[str]] = ...) -> None: ...

class ErrorCode(_message.Message):
    __slots__ = ("last_time", "error", "warn", "setting", "new_code", "battery", "obstacle_reminder")
    class NewCode(_message.Message):
        __slots__ = ("error", "warn")
        ERROR_FIELD_NUMBER: _ClassVar[int]
        WARN_FIELD_NUMBER: _ClassVar[int]
        error: _containers.RepeatedScalarFieldContainer[int]
        warn: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, error: _Optional[_Iterable[int]] = ..., warn: _Optional[_Iterable[int]] = ...) -> None: ...
    class Battery(_message.Message):
        __slots__ = ("restored",)
        RESTORED_FIELD_NUMBER: _ClassVar[int]
        restored: bool
        def __init__(self, restored: _Optional[bool] = ...) -> None: ...
    class ObstacleReminder(_message.Message):
        __slots__ = ("type", "photo_id", "accuracy", "map_id", "point")
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            POOP: _ClassVar[ErrorCode.ObstacleReminder.Type]
        POOP: ErrorCode.ObstacleReminder.Type
        TYPE_FIELD_NUMBER: _ClassVar[int]
        PHOTO_ID_FIELD_NUMBER: _ClassVar[int]
        ACCURACY_FIELD_NUMBER: _ClassVar[int]
        MAP_ID_FIELD_NUMBER: _ClassVar[int]
        POINT_FIELD_NUMBER: _ClassVar[int]
        type: ErrorCode.ObstacleReminder.Type
        photo_id: str
        accuracy: int
        map_id: int
        point: _common_pb2.Point
        def __init__(self, type: _Optional[_Union[ErrorCode.ObstacleReminder.Type, str]] = ..., photo_id: _Optional[str] = ..., accuracy: _Optional[int] = ..., map_id: _Optional[int] = ..., point: _Optional[_Union[_common_pb2.Point, _Mapping]] = ...) -> None: ...
    LAST_TIME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    WARN_FIELD_NUMBER: _ClassVar[int]
    SETTING_FIELD_NUMBER: _ClassVar[int]
    NEW_CODE_FIELD_NUMBER: _ClassVar[int]
    BATTERY_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_REMINDER_FIELD_NUMBER: _ClassVar[int]
    last_time: int
    error: _containers.RepeatedScalarFieldContainer[int]
    warn: _containers.RepeatedScalarFieldContainer[int]
    setting: ErrorSetting
    new_code: ErrorCode.NewCode
    battery: ErrorCode.Battery
    obstacle_reminder: _containers.RepeatedCompositeFieldContainer[ErrorCode.ObstacleReminder]
    def __init__(self, last_time: _Optional[int] = ..., error: _Optional[_Iterable[int]] = ..., warn: _Optional[_Iterable[int]] = ..., setting: _Optional[_Union[ErrorSetting, _Mapping]] = ..., new_code: _Optional[_Union[ErrorCode.NewCode, _Mapping]] = ..., battery: _Optional[_Union[ErrorCode.Battery, _Mapping]] = ..., obstacle_reminder: _Optional[_Iterable[_Union[ErrorCode.ObstacleReminder, _Mapping]]] = ...) -> None: ...

class PromptCode(_message.Message):
    __slots__ = ("last_time", "value")
    LAST_TIME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    last_time: int
    value: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, last_time: _Optional[int] = ..., value: _Optional[_Iterable[int]] = ...) -> None: ...
