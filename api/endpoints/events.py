from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from schemas.event import Event, EventCreate
from services.eventService import EventService
from dependencies.database import get_db
from dependencies.auth import get_current_user
from models.user import User as UserModel

router = APIRouter()


@router.get("/", response_model=List[Event])
def list_events(db: Session = Depends(get_db)):
    return EventService.get_events(db)


@router.post("/", response_model=Event)
def create_new_event(
    # request: Request,
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        # user_id = request.state.user_id
        created_event = EventService.create_event(db, event, current_user.id)
        return created_event
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.get("/{id}", response_model=Event)
def read_event(id: int, db: Session = Depends(get_db)):
    db_event = EventService.get_event(db, event_id=id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event
