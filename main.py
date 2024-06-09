from fastapi import FastAPI
from api.endpoints import bookings, events
from db.session import engine, create_database
from db.base import Base

app = FastAPI()

# Include routers
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

# Create the database if it doesn't exist
create_database()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Manager API"}
