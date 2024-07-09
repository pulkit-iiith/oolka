from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


class TransactionManager:
    @staticmethod
    def commit_with_refresh(db: Session, instance):
        try:
            db.commit()
            db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            db.rollback()
            print(f"SQLAlchemy Error: {str(e)}")
            raise HTTPException(status_code=500, detail="Transaction failed") from e
