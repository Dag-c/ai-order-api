from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate

def create_user(db: Session, user_data: UserCreate, hashed_password):
    user = User(
        email = user_data.email,
        password_hash = hashed_password,
        role = user_data.role
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user

def get_user_by_email(db: Session, email: str):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )