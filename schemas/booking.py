from pydantic import BaseModel

class BookingRequest(BaseModel):
    tickets: int
    payment_source: str

class BookingResponse(BaseModel):
    message: str
    event_id: int
    booked_tickets: int