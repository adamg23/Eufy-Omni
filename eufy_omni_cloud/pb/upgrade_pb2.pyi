from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryUpgradeStatus(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpgradeStatus(_message.Message):
    __slots__ = ("status", "progress", "error")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IDLE: _ClassVar[UpgradeStatus.Status]
        DOWNLOADING: _ClassVar[UpgradeStatus.Status]
        DOWNLOAD_COMPLETE: _ClassVar[UpgradeStatus.Status]
        DOWNLOAD_FAILED: _ClassVar[UpgradeStatus.Status]
        INSTALLING: _ClassVar[UpgradeStatus.Status]
        INSTALL_COMPLETE: _ClassVar[UpgradeStatus.Status]
        INSTALL_FAILED: _ClassVar[UpgradeStatus.Status]
    IDLE: UpgradeStatus.Status
    DOWNLOADING: UpgradeStatus.Status
    DOWNLOAD_COMPLETE: UpgradeStatus.Status
    DOWNLOAD_FAILED: UpgradeStatus.Status
    INSTALLING: UpgradeStatus.Status
    INSTALL_COMPLETE: UpgradeStatus.Status
    INSTALL_FAILED: UpgradeStatus.Status
    class Error(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[UpgradeStatus.Error]
        NOT_IN_STATION: _ClassVar[UpgradeStatus.Error]
        BATTERY_NOT_ENOUGH: _ClassVar[UpgradeStatus.Error]
        MCU_INSTALL_FAILED: _ClassVar[UpgradeStatus.Error]
        AP_INSTALL_FAILED: _ClassVar[UpgradeStatus.Error]
        STATION_NOT_CONNECTED: _ClassVar[UpgradeStatus.Error]
        STATION_INSTALL_FAILED: _ClassVar[UpgradeStatus.Error]
    NONE: UpgradeStatus.Error
    NOT_IN_STATION: UpgradeStatus.Error
    BATTERY_NOT_ENOUGH: UpgradeStatus.Error
    MCU_INSTALL_FAILED: UpgradeStatus.Error
    AP_INSTALL_FAILED: UpgradeStatus.Error
    STATION_NOT_CONNECTED: UpgradeStatus.Error
    STATION_INSTALL_FAILED: UpgradeStatus.Error
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    status: UpgradeStatus.Status
    progress: int
    error: str
    def __init__(self, status: _Optional[_Union[UpgradeStatus.Status, str]] = ..., progress: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...
