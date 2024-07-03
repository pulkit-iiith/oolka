from pydantic import BaseModel

class BookingRequest(BaseModel):
    tickets: int
    success_url: str
    cancel_url: str

class BookingResponse(BaseModel):
    message: str
    event_id: int
    booked_tickets: int
    payment_url: str