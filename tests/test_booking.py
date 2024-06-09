import pytest
from fastapi.testclient import TestClient
from main import app
from models.event import Event as EventModel
from dependencies.database import get_db
from db.base import Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from utils.test_data import event_data, booking_data, tickets_not_available_data

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_booking(setup_db):    
    client.post("/events/", json=event_data)
    response = client.post("/bookings/1/book", json=booking_data)    
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Booking successful"
    assert data["event_id"] == 1
    assert data["booked_tickets"] == 1

def test_create_booking_ticket_not_available(setup_db):    
    response = client.post("/bookings/1/book", json=tickets_not_available_data)    
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "Not enough tickets available"

def test_create_booking_event_not_present(setup_db):    
    response = client.post("/bookings/2/book", json=tickets_not_available_data)    
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Event not found"    
    