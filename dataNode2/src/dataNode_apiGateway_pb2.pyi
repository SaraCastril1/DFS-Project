from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WriteFileRequestData(_message.Message):
    __slots__ = ["folder", "filename", "file_data"]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    folder: str
    filename: str
    file_data: _wrappers_pb2.BytesValue
    def __init__(self, folder: _Optional[str] = ..., filename: _Optional[str] = ..., file_data: _Optional[_Union[_wrappers_pb2.BytesValue, _Mapping]] = ...) -> None: ...

class WriteFileResponseData(_message.Message):
    __slots__ = ["file_id", "data_node_addresses"]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_NODE_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    data_node_addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, file_id: _Optional[str] = ..., data_node_addresses: _Optional[_Iterable[str]] = ...) -> None: ...

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
