from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat_request_schema import ChatRequest
from app.services.chat_service import process_chat
from app.core.rate_limiter import check_rate_limit

router = APIRouter()


@router.post("/")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    allowed = check_rate_limit(
        request.session_id
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again in a minute."
        )

    response = await process_chat(
        session_id=request.session_id,
        message=request.message,
        db=db
    )

    return response