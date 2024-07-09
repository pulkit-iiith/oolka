from fastapi import FastAPI
from db.session import engine, create_database
from db.base import Base
from utils.middleware import AuthMiddleware
from api.endpoints import events, bookings, users
from utils.JWTManager import JWTManager
import os
import subprocess

# Initialize FastAPI app
app = FastAPI()

# Initialize JWTManager
jwt_manager = JWTManager(
    secret_key=os.getenv("SECRET_KEY"),
    algorithm=os.getenv("ALGORITHM"),
    access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
)

# Apply AuthMiddleware to the app
app.add_middleware(AuthMiddleware, jwt_manager=jwt_manager)

# Include routers
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Create the database if it doesn't exist
create_database()


# Create database tables
# Run Alembic migrations programmatically
# def run_alembic_migrations():
#     try:
#         subprocess.run(["alembic", "upgrade", "head"], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Alembic migration failed: {e}")
#         raise


# run_alembic_migrations()
# Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Manager API"}
