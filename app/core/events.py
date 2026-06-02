from app.core.session_store import redis_client
import json

ORDERS_CHANNEL = "orders"

def publish_order_event(event_type: str, data: dict):
    payload = {
        "type": event_type,
        "data": data
    }

    redis_client.publish(
        ORDERS_CHANNEL,
        json.dumps(payload)
    )