from pydantic import BaseModel
from datetime import datetime
from utils.enum import EventType
from typing import Optional

class EventBase(BaseModel):
    name: str
    date: datetime
    location: str
    total_tickets: int
    ticket_price: int
    place_lat: Optional[str] = None
    place_lng: Optional[str] = None
    event_type: EventType


class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    available_tickets: int

    class Config:
        orm_mode = True
