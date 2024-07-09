from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database as _create_database

load_dotenv()


MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_HOST = os.getenv("MYSQL_HOST")

# MySQL connection URL
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)

# Create the MySQL engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Function to create the database if it doesn't exist
def create_database():
    if not database_exists(engine.url):
        _create_database(engine.url)


# Create a session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_url():
    return SQLALCHEMY_DATABASE_URL
