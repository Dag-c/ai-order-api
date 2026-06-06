import time
import uuid

from app.core.session_store import redis_client

LIMIT = 10
WINDOW = 60


def check_rate_limit(key: str) -> bool:
    """
    Returns True if request is allowed.
    Returns False if rate limit exceeded.
    """

    now = int(time.time())

    redis_key = f"rate_limit:{key}"

    # Remove entries older than the window
    redis_client.zremrangebyscore(
        redis_key,
        0,
        now - WINDOW
    )

    current_requests = redis_client.zcard(redis_key)

    if current_requests >= LIMIT:
        return False

    member = f"{now}:{uuid.uuid4()}"

    redis_client.zadd(
        redis_key,
        {member: now}
    )

    redis_client.expire(
        redis_key,
        WINDOW
    )

    return True