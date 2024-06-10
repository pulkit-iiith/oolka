from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SqlEnum
from db.base import Base
from utils.enum import EventType

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True) 
    date = Column(DateTime)
    location = Column(String(255))
    total_tickets = Column(Integer)
    available_tickets = Column(Integer)
    ticket_price = Column(Integer)
    event_type = Column(SqlEnum(EventType), nullable=False)

