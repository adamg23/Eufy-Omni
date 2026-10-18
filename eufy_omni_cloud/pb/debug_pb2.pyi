from . import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DebugRequest(_message.Message):
    __slots__ = ("log_sw", "fault_report", "capture_sw", "image_feedback", "toggle_mop_raise", "toggle_mop_spin")
    class FaultReport(_message.Message):
        __slots__ = ("seq",)
        SEQ_FIELD_NUMBER: _ClassVar[int]
        seq: int
        def __init__(self, seq: _Optional[int] = ...) -> None: ...
    class ImageFeedback(_message.Message):
        __slots__ = ("object_type", "photo_id")
        OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
        PHOTO_ID_FIELD_NUMBER: _ClassVar[int]
        object_type: str
        photo_id: str
        def __init__(self, object_type: _Optional[str] = ..., photo_id: _Optional[str] = ...) -> None: ...
    LOG_SW_FIELD_NUMBER: _ClassVar[int]
    FAULT_REPORT_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_SW_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    TOGGLE_MOP_RAISE_FIELD_NUMBER: _ClassVar[int]
    TOGGLE_MOP_SPIN_FIELD_NUMBER: _ClassVar[int]
    log_sw: _common_pb2.Switch
    fault_report: DebugRequest.FaultReport
    capture_sw: _common_pb2.Switch
    image_feedback: DebugRequest.ImageFeedback
    toggle_mop_raise: _common_pb2.Switch
    toggle_mop_spin: _common_pb2.Switch
    def __init__(self, log_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ..., fault_report: _Optional[_Union[DebugRequest.FaultReport, _Mapping]] = ..., capture_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ..., image_feedback: _Optional[_Union[DebugRequest.ImageFeedback, _Mapping]] = ..., toggle_mop_raise: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ..., toggle_mop_spin: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ...) -> None: ...

class DebugResponse(_message.Message):
    __slots__ = ("log_sw", "update_info", "webtty_info", "capture_sw")
    class UpdateInfo(_message.Message):
        __slots__ = ("err_code",)
        ERR_CODE_FIELD_NUMBER: _ClassVar[int]
        err_code: int
        def __init__(self, err_code: _Optional[int] = ...) -> None: ...
    class WebTtyInfo(_message.Message):
        __slots__ = ("connection_data",)
        CONNECTION_DATA_FIELD_NUMBER: _ClassVar[int]
        connection_data: str
        def __init__(self, connection_data: _Optional[str] = ...) -> None: ...
    LOG_SW_FIELD_NUMBER: _ClassVar[int]
    UPDATE_INFO_FIELD_NUMBER: _ClassVar[int]
    WEBTTY_INFO_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_SW_FIELD_NUMBER: _ClassVar[int]
    log_sw: _common_pb2.Switch
    update_info: DebugResponse.UpdateInfo
    webtty_info: DebugResponse.WebTtyInfo
    capture_sw: _common_pb2.Switch
    def __init__(self, log_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ..., update_info: _Optional[_Union[DebugResponse.UpdateInfo, _Mapping]] = ..., webtty_info: _Optional[_Union[DebugResponse.WebTtyInfo, _Mapping]] = ..., capture_sw: _Optional[_Union[_common_pb2.Switch, _Mapping]] = ...) -> None: ...
