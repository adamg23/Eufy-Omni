from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MediaSetting(_message.Message):
    __slots__ = ("rt_stream", "record", "capture")
    class Resolution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        R_480P: _ClassVar[MediaSetting.Resolution]
        R_720P: _ClassVar[MediaSetting.Resolution]
        R_1080P: _ClassVar[MediaSetting.Resolution]
    R_480P: MediaSetting.Resolution
    R_720P: MediaSetting.Resolution
    R_1080P: MediaSetting.Resolution
    class RTStream(_message.Message):
        __slots__ = ("resolution",)
        RESOLUTION_FIELD_NUMBER: _ClassVar[int]
        resolution: MediaSetting.Resolution
        def __init__(self, resolution: _Optional[_Union[MediaSetting.Resolution, str]] = ...) -> None: ...
    class Record(_message.Message):
        __slots__ = ("resolution", "bitrate")
        RESOLUTION_FIELD_NUMBER: _ClassVar[int]
        BITRATE_FIELD_NUMBER: _ClassVar[int]
        resolution: MediaSetting.Resolution
        bitrate: int
        def __init__(self, resolution: _Optional[_Union[MediaSetting.Resolution, str]] = ..., bitrate: _Optional[int] = ...) -> None: ...
    class Capture(_message.Message):
        __slots__ = ("width", "height")
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        width: int
        height: int
        def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...
    RT_STREAM_FIELD_NUMBER: _ClassVar[int]
    RECORD_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_FIELD_NUMBER: _ClassVar[int]
    rt_stream: MediaSetting.RTStream
    record: MediaSetting.Record
    capture: MediaSetting.Capture
    def __init__(self, rt_stream: _Optional[_Union[MediaSetting.RTStream, _Mapping]] = ..., record: _Optional[_Union[MediaSetting.Record, _Mapping]] = ..., capture: _Optional[_Union[MediaSetting.Capture, _Mapping]] = ...) -> None: ...

class MediaStatus(_message.Message):
    __slots__ = ("state", "storage", "total_space", "photo_space", "video_space", "bind_state")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IDLE: _ClassVar[MediaStatus.State]
        RECORDING: _ClassVar[MediaStatus.State]
    IDLE: MediaStatus.State
    RECORDING: MediaStatus.State
    class Storage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NORMAL: _ClassVar[MediaStatus.Storage]
        THRESHOLD: _ClassVar[MediaStatus.Storage]
        FULL: _ClassVar[MediaStatus.Storage]
    NORMAL: MediaStatus.Storage
    THRESHOLD: MediaStatus.Storage
    FULL: MediaStatus.Storage
    STATE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SPACE_FIELD_NUMBER: _ClassVar[int]
    PHOTO_SPACE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_SPACE_FIELD_NUMBER: _ClassVar[int]
    BIND_STATE_FIELD_NUMBER: _ClassVar[int]
    state: MediaStatus.State
    storage: MediaStatus.Storage
    total_space: int
    photo_space: int
    video_space: int
    bind_state: bool
    def __init__(self, state: _Optional[_Union[MediaStatus.State, str]] = ..., storage: _Optional[_Union[MediaStatus.Storage, str]] = ..., total_space: _Optional[int] = ..., photo_space: _Optional[int] = ..., video_space: _Optional[int] = ..., bind_state: _Optional[bool] = ...) -> None: ...

class MediaManagerRequest(_message.Message):
    __slots__ = ("control", "setting", "bind_media_svc_data")
    class Control(_message.Message):
        __slots__ = ("method", "seq")
        class Method(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            RECORD_START: _ClassVar[MediaManagerRequest.Control.Method]
            RECORD_STOP: _ClassVar[MediaManagerRequest.Control.Method]
            CAPTURE: _ClassVar[MediaManagerRequest.Control.Method]
        RECORD_START: MediaManagerRequest.Control.Method
        RECORD_STOP: MediaManagerRequest.Control.Method
        CAPTURE: MediaManagerRequest.Control.Method
        METHOD_FIELD_NUMBER: _ClassVar[int]
        SEQ_FIELD_NUMBER: _ClassVar[int]
        method: MediaManagerRequest.Control.Method
        seq: int
        def __init__(self, method: _Optional[_Union[MediaManagerRequest.Control.Method, str]] = ..., seq: _Optional[int] = ...) -> None: ...
    class BindMediaSvc(_message.Message):
        __slots__ = ("seq", "c", "d", "g", "j", "user_account")
        SEQ_FIELD_NUMBER: _ClassVar[int]
        C_FIELD_NUMBER: _ClassVar[int]
        D_FIELD_NUMBER: _ClassVar[int]
        G_FIELD_NUMBER: _ClassVar[int]
        J_FIELD_NUMBER: _ClassVar[int]
        USER_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
        seq: int
        c: int
        d: int
        g: str
        j: int
        user_account: str
        def __init__(self, seq: _Optional[int] = ..., c: _Optional[int] = ..., d: _Optional[int] = ..., g: _Optional[str] = ..., j: _Optional[int] = ..., user_account: _Optional[str] = ...) -> None: ...
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    SETTING_FIELD_NUMBER: _ClassVar[int]
    BIND_MEDIA_SVC_DATA_FIELD_NUMBER: _ClassVar[int]
    control: MediaManagerRequest.Control
    setting: MediaSetting
    bind_media_svc_data: MediaManagerRequest.BindMediaSvc
    def __init__(self, control: _Optional[_Union[MediaManagerRequest.Control, _Mapping]] = ..., setting: _Optional[_Union[MediaSetting, _Mapping]] = ..., bind_media_svc_data: _Optional[_Union[MediaManagerRequest.BindMediaSvc, _Mapping]] = ...) -> None: ...

class MediaManagerResponse(_message.Message):
    __slots__ = ("control", "setting", "status", "bind_media_svc")
    class Control(_message.Message):
        __slots__ = ("method", "seq", "result", "file_info")
        class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SUCCESS: _ClassVar[MediaManagerResponse.Control.Result]
            FAIL: _ClassVar[MediaManagerResponse.Control.Result]
        SUCCESS: MediaManagerResponse.Control.Result
        FAIL: MediaManagerResponse.Control.Result
        class FileInfo(_message.Message):
            __slots__ = ("filepath", "id")
            FILEPATH_FIELD_NUMBER: _ClassVar[int]
            ID_FIELD_NUMBER: _ClassVar[int]
            filepath: str
            id: str
            def __init__(self, filepath: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...
        METHOD_FIELD_NUMBER: _ClassVar[int]
        SEQ_FIELD_NUMBER: _ClassVar[int]
        RESULT_FIELD_NUMBER: _ClassVar[int]
        FILE_INFO_FIELD_NUMBER: _ClassVar[int]
        method: MediaManagerRequest.Control.Method
        seq: int
        result: MediaManagerResponse.Control.Result
        file_info: MediaManagerResponse.Control.FileInfo
        def __init__(self, method: _Optional[_Union[MediaManagerRequest.Control.Method, str]] = ..., seq: _Optional[int] = ..., result: _Optional[_Union[MediaManagerResponse.Control.Result, str]] = ..., file_info: _Optional[_Union[MediaManagerResponse.Control.FileInfo, _Mapping]] = ...) -> None: ...
    class BindMediaSvc(_message.Message):
        __slots__ = ("seq", "result")
        class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SUCCESS: _ClassVar[MediaManagerResponse.BindMediaSvc.Result]
            FAIL: _ClassVar[MediaManagerResponse.BindMediaSvc.Result]
        SUCCESS: MediaManagerResponse.BindMediaSvc.Result
        FAIL: MediaManagerResponse.BindMediaSvc.Result
        SEQ_FIELD_NUMBER: _ClassVar[int]
        RESULT_FIELD_NUMBER: _ClassVar[int]
        seq: int
        result: MediaManagerResponse.BindMediaSvc.Result
        def __init__(self, seq: _Optional[int] = ..., result: _Optional[_Union[MediaManagerResponse.BindMediaSvc.Result, str]] = ...) -> None: ...
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    SETTING_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BIND_MEDIA_SVC_FIELD_NUMBER: _ClassVar[int]
    control: MediaManagerResponse.Control
    setting: MediaSetting
    status: MediaStatus
    bind_media_svc: MediaManagerResponse.BindMediaSvc
    def __init__(self, control: _Optional[_Union[MediaManagerResponse.Control, _Mapping]] = ..., setting: _Optional[_Union[MediaSetting, _Mapping]] = ..., status: _Optional[_Union[MediaStatus, _Mapping]] = ..., bind_media_svc: _Optional[_Union[MediaManagerResponse.BindMediaSvc, _Mapping]] = ...) -> None: ...
