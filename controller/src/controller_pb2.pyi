from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Nada(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Response(_message.Message):
    __slots__ = ["cpu_usage", "status_code"]
    CPU_USAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    cpu_usage: int
    status_code: int
    def __init__(self, status_code: _Optional[int] = ..., cpu_usage: _Optional[int] = ...) -> None: ...
