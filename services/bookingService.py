from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.event import Event as EventModel
from schemas.booking import BookingResponse
from db.transaction import TransactionManager
from services.payment.payment_service import PaymentService
from services.payment.stripe_payment_processor import StripeAdapter

class BookingService:
    @staticmethod
    def book_tickets(db: Session, event_id: int, tickets: int, payment_source: float) -> BookingResponse:
        event = db.query(EventModel).filter(EventModel.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        if event.available_tickets < tickets:
            raise HTTPException(status_code=400, detail="Not enough tickets available")
        

        # Calculate total cost
        total_cost = tickets * event.ticket_price

        stripe_adapter = StripeAdapter(api_key="your_stripe_secret_key")
        payment_service = PaymentService(processor=stripe_adapter)
        try:
            payment_service.process_payment(
                amount=int(total_cost * 100),  # Stripe expects the amount in cents
                currency="usd",
                source=payment_source,
                description=f"Booking for event {event.name}"
            )
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

        # Update ticket availability
        event.available_tickets -= tickets
        TransactionManager.commit_with_refresh(db, event)
        
        return BookingResponse(
            message="Booking successful",
            event_id=event.id,
            booked_tickets=tickets
        )
