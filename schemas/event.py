from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    name: str
    date: datetime
    location: str
    total_tickets: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    available_tickets: int

    class Config:
        orm_mode = True
