from sqlalchemy import Column, Integer, String, Date
from db.base import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    # name = Column(String, index=True)
    name = Column(String(255), index=True) 
    date = Column(Date)
    location = Column(String(255))
    total_tickets = Column(Integer)
    available_tickets = Column(Integer)
