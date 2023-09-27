from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WriteFileRequest(_message.Message):
    __slots__ = ["folder", "filename"]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    folder: str
    filename: str
    def __init__(self, folder: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class WriteFileResponse(_message.Message):
    __slots__ = ["file_id", "data_node_addresses"]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_NODE_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    data_node_addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, file_id: _Optional[str] = ..., data_node_addresses: _Optional[_Iterable[str]] = ...) -> None: ...

class ReadFileRequest(_message.Message):
    __slots__ = ["folder", "filename"]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    folder: str
    filename: str
    def __init__(self, folder: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class ReadFileResponse(_message.Message):
    __slots__ = ["file_id", "data_node_addresses"]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_NODE_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    data_node_addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, file_id: _Optional[str] = ..., data_node_addresses: _Optional[_Iterable[str]] = ...) -> None: ...

class ListFilesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListFilesResponse(_message.Message):
    __slots__ = ["filenames"]
    FILENAMES_FIELD_NUMBER: _ClassVar[int]
    filenames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, filenames: _Optional[_Iterable[str]] = ...) -> None: ...
