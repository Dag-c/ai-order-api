from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jose import jwt 
from app.core.config import SECRET_APP_KEY, ALGORITHM

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=8)

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_APP_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt