from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LanguageRequest(_message.Message):
    __slots__ = ("desc", "selection")
    class Desc(_message.Message):
        __slots__ = ("set_id", "url", "md5", "version", "size")
        SET_ID_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        MD5_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        set_id: int
        url: str
        md5: str
        version: int
        size: int
        def __init__(self, set_id: _Optional[int] = ..., url: _Optional[str] = ..., md5: _Optional[str] = ..., version: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...
    class Selection(_message.Message):
        __slots__ = ("value",)
        class Value(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            DEFAULT: _ClassVar[LanguageRequest.Selection.Value]
            USER: _ClassVar[LanguageRequest.Selection.Value]
        DEFAULT: LanguageRequest.Selection.Value
        USER: LanguageRequest.Selection.Value
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: LanguageRequest.Selection.Value
        def __init__(self, value: _Optional[_Union[LanguageRequest.Selection.Value, str]] = ...) -> None: ...
    DESC_FIELD_NUMBER: _ClassVar[int]
    SELECTION_FIELD_NUMBER: _ClassVar[int]
    desc: LanguageRequest.Desc
    selection: LanguageRequest.Selection
    def __init__(self, desc: _Optional[_Union[LanguageRequest.Desc, _Mapping]] = ..., selection: _Optional[_Union[LanguageRequest.Selection, _Mapping]] = ...) -> None: ...

class LanguageResponse(_message.Message):
    __slots__ = ("default_id", "current_id", "version", "set_id", "state")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IDLE: _ClassVar[LanguageResponse.State]
        UPDATING: _ClassVar[LanguageResponse.State]
        SUCCESS: _ClassVar[LanguageResponse.State]
        FAILURE: _ClassVar[LanguageResponse.State]
    IDLE: LanguageResponse.State
    UPDATING: LanguageResponse.State
    SUCCESS: LanguageResponse.State
    FAILURE: LanguageResponse.State
    DEFAULT_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SET_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    default_id: int
    current_id: int
    version: int
    set_id: int
    state: LanguageResponse.State
    def __init__(self, default_id: _Optional[int] = ..., current_id: _Optional[int] = ..., version: _Optional[int] = ..., set_id: _Optional[int] = ..., state: _Optional[_Union[LanguageResponse.State, str]] = ...) -> None: ...
