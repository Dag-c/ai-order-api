from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db

from app.schemas.auth_schema import LoginSchema

from app.services.auth_service import (
    login_service
)

router = APIRouter()

# Testing user
"""{
  "email": "diego.guillen.d.cruz@gmail.com",
  "password": "Guillen7"
}
"""

@router.post("/")
def login(
    credentials: LoginSchema,
    db: Session = Depends(get_db)
):

    return login_service(
        db,
        credentials.email,
        credentials.password
    )