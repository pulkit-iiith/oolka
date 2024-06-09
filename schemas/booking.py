from pydantic import BaseModel

class BookingRequest(BaseModel):
    tickets: int

class BookingResponse(BaseModel):
    message: str
    event_id: int
    booked_tickets: int