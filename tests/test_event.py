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
from utils.test_data import event_data

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

def test_create_new_event(setup_db):    
    response = client.post("/events/", json=event_data)    
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test Event"
    assert data["date"] == "2023-12-31T00:00:00"
    assert data["location"] == "Test Location"
    assert data["total_tickets"] == 100
    assert data["available_tickets"] == 100
    assert data["event_type"] == "music festival"

def test_list_events(setup_db):
    response = client.get("/events/")
    assert response.status_code == 200
    data = response.json()
    assert data == [{'name': 'Test Event', 'location': 'Test Location', 'total_tickets': 100, 'available_tickets': 100, 'date': '2023-12-31T00:00:00', 'event_type': 'music festival', 'id': 1}]

def test_get_events(setup_db):
    response = client.get("/events/1")
    assert response.status_code == 200
    data = response.json()
    assert data == {'name': 'Test Event', 'location': 'Test Location', 'total_tickets': 100, 'available_tickets': 100, 'date': '2023-12-31T00:00:00', 'event_type': 'music festival', 'id': 1}


def test_create_duplicate_event(setup_db):
    client.post("/events/", json=event_data)
    response = client.post("/events/", json=event_data)
    assert response.status_code == 400
    data = response.json()
    assert data == {"detail": "An event with the name 'Test Event' on date '2023-12-31 00:00:00' already exists."}
