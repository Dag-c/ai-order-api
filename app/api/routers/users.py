from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db

from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user_service

router = APIRouter()

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user_service(db, user)

    return {
        "message": "User created",
        "user": {
            "id": str(new_user.id),
            "email": new_user.email
        }
    }
