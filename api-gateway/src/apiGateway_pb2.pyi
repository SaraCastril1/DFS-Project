from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReadFileRequestData(_message.Message):
    __slots__ = ["file_name"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    def __init__(self, file_name: _Optional[str] = ...) -> None: ...

class ReadFileResponseData(_message.Message):
    __slots__ = ["file_data"]
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    file_data: bytes
    def __init__(self, file_data: _Optional[bytes] = ...) -> None: ...
