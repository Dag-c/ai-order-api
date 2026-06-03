import asyncio
import json
import logging

from app.core.session_store import redis_client
from app.core.websocket_manager import manager

logger = logging.getLogger(__name__)

ORDERS_CHANNEL = "orders"

async def redis_listener():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(ORDERS_CHANNEL)

    logger.info("Redis listener started")

    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)

            if not message:
                await asyncio.sleep(0.5)
                continue

            if message["type"] != "message":
                continue

            data = json.loads(message["data"])

            logger.info("Redis event received: %s", data)

            await manager.broadcast(data)

    except asyncio.CancelledError:
        logger.info("Redis listener shutting down")

    finally:
        pubsub.close()