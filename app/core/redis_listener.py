import asyncio
import json

from app.core.session_store import redis_client
from app.core.websocket_manager import manager

ORDERS_CHANNEL = "orders"


async def redis_listener():
    pubsub = redis_client.pubsub()

    pubsub.subscribe(ORDERS_CHANNEL)

    print("🟢 Redis listener iniciado...")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)

        if message:
            try:
                if message["type"] != "message":
                    continue

                data = json.loads(message["data"])

                print("📩 Evento recibido:", data)

                await manager.broadcast(data)

            except Exception as e:
                print("❌ Error procesando mensaje:", e)

        await asyncio.sleep(0.5)