from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User as UserModel
from schemas.user import UserCreate
from db.transaction import TransactionManager
import os
from utils.JWTManager import JWTManager

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # Check if user already exists by username or email
        existing_user = db.query(UserModel).filter(
            (UserModel.username == user.username) | (UserModel.email == user.email)
        ).first()

        if existing_user:
            user_id = existing_user.id
        else:

            # Create new user if no existing user found
            db_user = UserModel(
                username=user.username,
                email=user.email,
                hashed_password=user.password,  # Assume you have hashed the password appropriately
                is_admin=user.is_admin
            )
            db.add(db_user)
            TransactionManager.commit_with_refresh(db, db_user)
            user_id = db_user.id

        jwt_manager = JWTManager(
            secret_key=os.getenv("SECRET_KEY"),
            algorithm=os.getenv("ALGORITHM"),
            access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
        )

        # Create access token
        access_token = jwt_manager.create_access_token(user_id=user_id)

        return {
        "user_id": user_id,
        "access_token": access_token
    }
