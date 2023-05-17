from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EasyRequest(_message.Message):
    __slots__ = ["package"]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    package: str
    def __init__(self, package: _Optional[str] = ...) -> None: ...

class HardRequest(_message.Message):
    __slots__ = ["container", "package"]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    container: str
    package: str
    def __init__(self, package: _Optional[str] = ..., container: _Optional[str] = ...) -> None: ...

class NoRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
