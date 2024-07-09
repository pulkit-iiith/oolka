from enum import Enum


class EventType(str, Enum):
    MUSIC_FESTIVAL = "music festival"
    MOVIES = "movies"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
