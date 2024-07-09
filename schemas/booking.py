from pydantic import BaseModel
from utils.enum import PaymentStatus


class BookingBase(BaseModel):
    tickets: int
    userid: int
    payment_status: PaymentStatus


class BookingRequest(BaseModel):
    tickets: int
    success_url: str
    cancel_url: str
    payment_status: str = PaymentStatus


class BookingResponse(BaseModel):
    message: str
    event_id: int
    booked_tickets: int
    payment_url: str
    payment_status: PaymentStatus
    checkout_session_id: str
