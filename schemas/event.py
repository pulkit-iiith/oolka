from pydantic import BaseModel, Field
from datetime import datetime
from utils.enum import EventType
from typing import Optional


class EventBase(BaseModel):
    name: str
    date: datetime
    location: str
    total_tickets: int = Field(..., ge=0)
    ticket_price: int = Field(..., ge=0)
    event_type: EventType


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    available_tickets: int
    place_lat: str
    place_lng: str
    userid: int

    class Config:
        orm_mode = True
