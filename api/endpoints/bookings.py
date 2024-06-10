from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.booking import BookingRequest, BookingResponse
from services.bookingService import BookingService
from dependencies.database import get_db

router = APIRouter()

@router.post("/{event_id}/book", response_model=BookingResponse)
def book_event_tickets(event_id: int, booking: BookingRequest, db: Session = Depends(get_db)):
    return BookingService.book_tickets(db, event_id, booking.tickets,booking.payment_source)
