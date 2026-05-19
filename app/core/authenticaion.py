from jose import jwt, JWTError

from fastapi import Depends, HTTPException

from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.repositories.user_repository import (
    get_user_by_email
)

from app.core.security import (
    SECRET_APP_KEY,
    ALGORITHM
)

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_APP_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("email")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email)

    if user is None:
        raise credentials_exception

    return user