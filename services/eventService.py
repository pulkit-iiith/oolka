from sqlalchemy.orm import Session
from models.event import Event as EventModel
from schemas.event import EventCreate
from db.transaction import TransactionManager
from fastapi import HTTPException

class EventService:
    @staticmethod
    def get_events(db: Session):
        return db.query(EventModel).all()

    @staticmethod
    def get_event(db: Session, event_id: int):
        return db.query(EventModel).filter(EventModel.id == event_id).first()

    @staticmethod
    def create_event(db: Session, event: EventCreate):
        # Check if an event with the same name and date already exists
        existing_event = db.query(EventModel).filter(
            EventModel.name == event.name,
            EventModel.date == event.date,
            EventModel.event_type == event.event_type
        ).first()

        if existing_event:
            # Raise an exception or return a response indicating duplication
            raise ValueError(f"An event with the name '{event.name}' on date '{event.date}' already exists.")

        # If no duplicate is found, proceed to create the event
        db_event = EventModel(
            name=event.name,
            date=event.date,
            location=event.location,
            total_tickets=event.total_tickets,
            available_tickets=event.total_tickets,
            event_type=event.event_type
        )
        db.add(db_event)
        TransactionManager.commit_with_refresh(db, db_event)
        return db_event
