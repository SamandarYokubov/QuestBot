from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ("user_id", "course_name", "course_module", "question_type", "content_type")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_NAME_FIELD_NUMBER: _ClassVar[int]
    COURSE_MODULE_FIELD_NUMBER: _ClassVar[int]
    QUESTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    course_name: str
    course_module: int
    question_type: str
    content_type: str
    def __init__(self, user_id: _Optional[str] = ..., course_name: _Optional[str] = ..., course_module: _Optional[int] = ..., question_type: _Optional[str] = ..., content_type: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("questions",)
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    questions: str
    def __init__(self, questions: _Optional[str] = ...) -> None: ...
