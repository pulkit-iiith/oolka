from sqlalchemy.orm import Session
from models.event import Event as EventModel
from models.user import User as UserModel
from schemas.event import EventCreate
from db.transaction import TransactionManager
from fastapi import HTTPException
from services.adaptor.GoogleMapsAdapter import GoogleMapsAdapter

class EventService:
    @staticmethod
    def get_events(db: Session):
        return db.query(EventModel).all()

    @staticmethod
    def get_event(db: Session, event_id: int):
        return db.query(EventModel).filter(EventModel.id == event_id).first()

    @staticmethod
    def create_event(db: Session, event: EventCreate, user_id: int):
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.is_admin:
            raise HTTPException(status_code=403, detail="You do not have rights to create an event")
        
        # Check if an event with the same name and date already exists
        existing_event = db.query(EventModel).filter(
            EventModel.name == event.name,
            EventModel.date == event.date,
            EventModel.event_type == event.event_type
        ).first()

        if existing_event:
            # Raise an exception or return a response indicating duplication
            raise ValueError(f"An event with the name '{event.name}' on date '{event.date}' already exists.")
        
        # Use the adapter to fetch latitude and longitude
        place_lat, place_lng = GoogleMapsAdapter.get_lat_lng(event.location)

        # If no duplicate is found, proceed to create the event
        db_event = EventModel(
            name=event.name,
            date=event.date,
            location=event.location,
            total_tickets=event.total_tickets,
            available_tickets=event.total_tickets,
            ticket_price=event.ticket_price,
            event_type=event.event_type,
            place_lat = place_lat,
            place_lng = place_lng
        )
        db.add(db_event)
        TransactionManager.commit_with_refresh(db, db_event)
        return db_event
