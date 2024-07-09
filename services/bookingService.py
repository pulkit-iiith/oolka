from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.event import Event as EventModel
from models.booking import Booking as BookingModel
from schemas.booking import BookingResponse
from db.transaction import TransactionManager
from utils.enum import PaymentStatus
from services.payment.payment_service import PaymentService
from services.payment.stripe_payment_processor import StripeAdapter


class BookingService:
    @staticmethod
    def calculate_dynamic_price(available_tickets: int, base_price: float) -> float:
        if available_tickets > 100:
            return base_price
        elif available_tickets > 50:
            return base_price * 1.1  # 10% increase
        elif available_tickets > 20:
            return base_price * 1.2  # 20% increase
        else:
            return base_price * 1.5  # 50% increase

    @staticmethod
    def book_tickets(
        db: Session,
        event_id: int,
        tickets: int,
        success_url: str,
        cancel_url: str,
        userid: int,
    ) -> BookingResponse:
        event = db.query(EventModel).filter(EventModel.id == event_id).first()
        if not event:
            raise ValueError("Event not found")
        if event.available_tickets < tickets:
            raise ValueError("Not enough tickets available")
        if tickets <= 0:
            raise ValueError("give non negative tickets to be booked")

        # Calculate total cost using dynamic pricing
        ticket_price = BookingService.calculate_dynamic_price(
            event.available_tickets, event.ticket_price
        )
        total_cost = tickets * ticket_price

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
                metadata={"user_id": userid, "event_id": event_id},
            )
            print(session, "*****************************")
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

        db_event = BookingModel(
            tickets=tickets,
            userid=userid,
            eventid=event_id,
            amount=total_cost,
            payment_status=PaymentStatus.PENDING,
            checkout_session_id=session["id"],
        )
        db.add(db_event)
        TransactionManager.commit_with_refresh(db, db_event)
        return BookingResponse(
            message="Booking successful",
            event_id=event.id,
            booked_tickets=tickets,
            payment_url=session["url"],
            payment_status=db_event.payment_status,
            checkout_session_id=session["id"],
        )
