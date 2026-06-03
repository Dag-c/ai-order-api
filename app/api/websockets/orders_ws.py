import asyncio
import logging

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from sqlalchemy.orm import Session

from app.core.websocket_manager import manager
from app.core.database import SessionLocal
from app.core.authenticaion import validate_token

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/orders")
async def orders_websocket(websocket: WebSocket):

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    # =========================
    # DATABASE SESSION
    # =========================
    db: Session = SessionLocal()

    try:

        # =========================
        # VALIDATE JWT
        # =========================
        validate_token(token, db)

        # =========================
        # ACCEPT CONNECTION
        # =========================
        await manager.connect(websocket)

        logger.info("WebSocket connected")

        while True:
            await asyncio.sleep(60)

    except Exception as e:

        logger.exception("WebSocket auth error")

        await websocket.close(code=1008)

    finally:

        manager.disconnect(websocket)

        db.close()

        logger.info("WebSocket disconnected")
