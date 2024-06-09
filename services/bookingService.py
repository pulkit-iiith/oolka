from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.event import Event as EventModel
from schemas.booking import BookingResponse
from db.transaction import TransactionManager

class BookingService:
    @staticmethod
    def book_tickets(db: Session, event_id: int, tickets: int) -> BookingResponse:
        event = db.query(EventModel).filter(EventModel.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        if event.available_tickets < tickets:
            raise HTTPException(status_code=400, detail="Not enough tickets available")

        event.available_tickets -= tickets
        TransactionManager.commit_with_refresh(db, event)
        
        return BookingResponse(
            message="Booking successful",
            event_id=event.id,
            booked_tickets=tickets
        )
