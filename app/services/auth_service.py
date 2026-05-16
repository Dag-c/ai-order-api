from fastapi import HTTPException

from app.repositories.user_repository import (
    get_user_by_email
)

from app.core.security import verify_password

from app.core.security import create_access_token


def login_service(db, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    valid_password = verify_password(
        password,
        user.password_hash
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }