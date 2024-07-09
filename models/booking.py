from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SqlEnum
from sqlalchemy.sql import func
from utils.enum import PaymentStatus
from db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    eventid = Column(Integer)
    tickets = Column(Integer)
    userid = Column(Integer)
    booking_time = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(Float, nullable=False)
    payment_status = Column(
        SqlEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING
    )
    checkout_session_id = Column(String(255))
