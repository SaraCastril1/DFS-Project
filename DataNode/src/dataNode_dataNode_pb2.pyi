from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReplicateFile(_message.Message):
    __slots__ = ["folder", "filename", "file_data"]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    folder: str
    filename: str
    file_data: bytes
    def __init__(self, folder: _Optional[str] = ..., filename: _Optional[str] = ..., file_data: _Optional[bytes] = ...) -> None: ...

class ReplicateFileResponse(_message.Message):
    __slots__ = ["replicated"]
    REPLICATED_FIELD_NUMBER: _ClassVar[int]
    replicated: str
    def __init__(self, replicated: _Optional[str] = ...) -> None: ...
