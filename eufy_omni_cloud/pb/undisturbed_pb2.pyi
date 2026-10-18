from . import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Undisturbed(_message.Message):
    __slots__ = ("sw", "begin", "end")
    class TimePoint(_message.Message):
        __slots__ = ("hour", "minute")
        HOUR_FIELD_NUMBER: _ClassVar[int]
        MINUTE_FIELD_NUMBER: _ClassVar[int]
        hour: int
        minute: int
        def __init__(self, hour: _Optional[int] = ..., minute: _Optional[int] = ...) -> None: ...
    SW_FIELD_NUMBER: _ClassVar[int]
    BEGIN_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    sw: _common_pb2.Switch
    begin: Undisturbed.TimePoint
    end: Undisturbed.TimePoint
    def __init__(self, sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ..., begin: _Optional[_Union[Undisturbed.TimePoint, _Mapping]] = ..., end: _Optional[_Union[Undisturbed.TimePoint, _Mapping]] = ...) -> None: ...

class UndisturbedRequest(_message.Message):
    __slots__ = ("undisturbed",)
    UNDISTURBED_FIELD_NUMBER: _ClassVar[int]
    undisturbed: Undisturbed
    def __init__(self, undisturbed: _Optional[_Union[Undisturbed, _Mapping]] = ...) -> None: ...

class UndisturbedResponse(_message.Message):
    __slots__ = ("active", "undisturbed")
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    UNDISTURBED_FIELD_NUMBER: _ClassVar[int]
    active: _common_pb2.Active
    undisturbed: Undisturbed
    def __init__(self, active: _Optional[_Union[_common_pb2.Active, _Mapping]] = ..., undisturbed: _Optional[_Union[Undisturbed, _Mapping]] = ...) -> None: ...
