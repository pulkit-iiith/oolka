from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.event import Event as EventModel
from schemas.booking import BookingResponse
from db.transaction import TransactionManager
from services.payment.payment_service import PaymentService
from services.payment.stripe_payment_processor import StripeAdapter


class BookingService:
    @staticmethod
    def book_tickets(
        db: Session, event_id: int, tickets: int, success_url: str, cancel_url: str
    ) -> BookingResponse:
        event = db.query(EventModel).filter(EventModel.id == event_id).first()
        if not event:
            raise ValueError("Event not found")
        if event.available_tickets < tickets:
            raise ValueError("Not enough tickets available")
        if tickets <= 0:
            raise ValueError("give non negative tickets to be booked")

        # Calculate total cost
        total_cost = tickets * event.ticket_price

        stripe_adapter = StripeAdapter(
            api_key="sk_test_51N04I3SFZ5NhuMix5R4gKyOGARimRCXCihXhZzoruDgWhuafxiE059kH4hGhvF6gLcdSniyk4Fi791AwEB9WymQI00ZWOCXEt5"
        )
        payment_service = PaymentService(processor=stripe_adapter)
        try:
            session = payment_service.create_checkout_session(
                amount=int(total_cost * 100),  # Stripe expects the amount in cents
                currency="inr",
                description=f"Booking for event {event.name}",
                success_url=success_url,
                cancel_url=cancel_url,
            )
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

        # Update ticket availability
        event.available_tickets -= tickets
        TransactionManager.commit_with_refresh(db, event)

        return BookingResponse(
            message="Booking successful",
            event_id=event.id,
            booked_tickets=tickets,
            payment_url=session["url"],
        )
