from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserUpdate
from app.repositories.user_repository import create_user
from app.core.security import hash_password

from uuid import UUID

def create_user_service(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    return create_user(db, user_data, hashed_password)