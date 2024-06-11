from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from models.user import User as UserModel
from dependencies.database import get_db

def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserModel:
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid user")
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user
