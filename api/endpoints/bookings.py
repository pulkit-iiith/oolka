from fastapi import APIRouter, Depends, HTTPException, Request
import stripe
from sqlalchemy.orm import Session
from schemas.booking import BookingRequest, BookingResponse
from services.bookingService import BookingService
from dependencies.database import get_db
from models.user import User as UserModel
from models.booking import Booking as BookingModel
from models.event import Event as EventModel
from dependencies.auth import get_current_user

router = APIRouter()

stripe.api_key = "sk_test_51N04I3SFZ5NhuMix5R4gKyOGARimRCXCihXhZzoruDgWhuafxiE059kH4hGhvF6gLcdSniyk4Fi791AwEB9WymQI00ZWOCXEt5"
endpoint_secret = "whsec_K1akzWQZo8bh14CHNSS6B7DpGc4VzVDF"


@router.post("/{event_id}/book", response_model=BookingResponse)
def book_event_tickets(
    event_id: int,
    booking: BookingRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        book_tickets = BookingService.book_tickets(
            db,
            event_id,
            booking.tickets,
            booking.success_url,
            booking.cancel_url,
            current_user.id,
        )
        return book_tickets
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.post("/webhook/")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    print("Webhook endpoint hit")
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # print(f"Received event: {event}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"Session data: {session}")
        checkout_session_id = session["id"]

        # Find the booking and update status
        booking = (
            db.query(BookingModel)
            .filter_by(
                checkout_session_id=checkout_session_id,
            )
            .first()
        )
        if booking:
            booking.payment_status = "completed"
            db.commit()
            # Reduce the available tickets after successful payment
            event = db.query(EventModel).filter_by(id=booking.eventid).first()
            if event:
                event.available_tickets -= booking.tickets
                db.commit()

    elif (
        event["type"] == "checkout.session.async_payment_failed"
        or event["type"] == "checkout.session.expired"
    ):
        session = event["data"]["object"]

        # Find the booking and update status
        booking = (
            db.query(BookingModel)
            .filter_by(
                checkout_session_id=checkout_session_id,
            )
            .first()
        )
        if booking:
            booking.payment_status = "failed"

    return {"status": "success"}
