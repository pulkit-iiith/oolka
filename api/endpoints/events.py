from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.event import Event, EventCreate
from services.eventService import EventService
from dependencies.database import get_db

router = APIRouter()

@router.get("/", response_model=List[Event])
def list_events(db: Session = Depends(get_db)):
    return EventService.get_events(db)

@router.post("/", response_model=Event)
def create_new_event(event: EventCreate, db: Session = Depends(get_db)):
    return EventService.create_event(db=db, event=event)

@router.get("/{id}", response_model=Event)
def read_event(id: int, db: Session = Depends(get_db)):
    db_event = EventService.get_event(db, event_id=id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event
