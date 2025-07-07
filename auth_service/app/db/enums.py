from enum import Enum, auto


class Role(Enum):
    ADMIN = auto()
    PARENT = auto()
    TEACHER = auto()
    STUDENT = auto()
