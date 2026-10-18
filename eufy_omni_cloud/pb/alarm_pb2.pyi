from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Alarm(_message.Message):
    __slots__ = ("hours", "minutes", "repetition", "week_info")
    HOURS_FIELD_NUMBER: _ClassVar[int]
    MINUTES_FIELD_NUMBER: _ClassVar[int]
    REPETITION_FIELD_NUMBER: _ClassVar[int]
    WEEK_INFO_FIELD_NUMBER: _ClassVar[int]
    hours: int
    minutes: int
    repetition: bool
    week_info: int
    def __init__(self, hours: _Optional[int] = ..., minutes: _Optional[int] = ..., repetition: _Optional[bool] = ..., week_info: _Optional[int] = ...) -> None: ...

class SyncTime(_message.Message):
    __slots__ = ("year", "month", "day", "weekday", "hours", "minutes", "seconds")
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    WEEKDAY_FIELD_NUMBER: _ClassVar[int]
    HOURS_FIELD_NUMBER: _ClassVar[int]
    MINUTES_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    year: int
    month: int
    day: int
    weekday: int
    hours: int
    minutes: int
    seconds: int
    def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., weekday: _Optional[int] = ..., hours: _Optional[int] = ..., minutes: _Optional[int] = ..., seconds: _Optional[int] = ...) -> None: ...
