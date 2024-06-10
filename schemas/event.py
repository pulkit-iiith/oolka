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
    event_type: EventType


class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    available_tickets: int
    place_lat: str
    place_lng: str

    class Config:
        orm_mode = True
