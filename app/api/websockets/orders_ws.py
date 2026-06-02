import asyncio

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from sqlalchemy.orm import Session

from app.core.websocket_manager import manager
from app.core.database import SessionLocal
from app.core.authenticaion import validate_token

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

        print("🟢 WS conectado")

        while True:
            await asyncio.sleep(60)

    except Exception as e:

        print("❌ WS auth error:", e)

        await websocket.close(code=1008)

    finally:

        manager.disconnect(websocket)

        db.close()

        print("🔴 WS desconectado")
