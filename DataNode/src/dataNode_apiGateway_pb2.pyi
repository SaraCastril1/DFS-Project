from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WriteFileRequestData(_message.Message):
    __slots__ = ["folder", "filename", "file_data", "create_folder"]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    CREATE_FOLDER_FIELD_NUMBER: _ClassVar[int]
    folder: str
    filename: str
    file_data: bytes
    create_folder: str
    def __init__(self, folder: _Optional[str] = ..., filename: _Optional[str] = ..., file_data: _Optional[bytes] = ..., create_folder: _Optional[str] = ...) -> None: ...

class WriteFileResponseData(_message.Message):
    __slots__ = ["write_success"]
    WRITE_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    write_success: bool
    def __init__(self, write_success: bool = ...) -> None: ...

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
