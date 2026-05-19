from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat_request_schema import ChatRequest
from app.services.chat_service import process_chat

router = APIRouter()


@router.post("/")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    response = await process_chat(
        session_id=request.session_id,
        message=request.message,
        db= db
    )

    return response