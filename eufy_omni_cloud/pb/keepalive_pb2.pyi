from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class KeepAliveRequest(_message.Message):
    __slots__ = ("timestamp", "force_sync")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FORCE_SYNC_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    force_sync: bool
    def __init__(self, timestamp: _Optional[int] = ..., force_sync: _Optional[bool] = ...) -> None: ...
