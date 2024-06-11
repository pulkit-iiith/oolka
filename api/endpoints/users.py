from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from services.userService import UserService
from dependencies.database import get_db
from utils.JWTManager import JWTManager

router = APIRouter()

SECRET_KEY = "your_jwt_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

jwt_manager = JWTManager(secret_key=SECRET_KEY, algorithm=ALGORITHM, access_token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

@router.post("/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)

