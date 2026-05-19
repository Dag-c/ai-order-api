import redis

from app.schemas.chat_session_schema import ChatSessionSchema
from app.core.config import REDIS_URL

# Redis client
redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True
)

SESSION_TTL_SECONDS = 60 * 60 

def get_session(session_id: str) -> ChatSessionSchema:
    """
    Download a session from Redis.
    If doesn't exists creat a new one.
    """
    data = redis_client.get(session_id)
    
    if data is None:
        session = ChatSessionSchema()
        save_session(session_id, session)
        return session
    
    return ChatSessionSchema.model_validate_json(data)

def save_session(session_id: str, session:ChatSessionSchema):
    """
    Store a session on Redis with TTL.
    """
    redis_client.setex(
        session_id,
        SESSION_TTL_SECONDS,
        session.model_dump_json()
    )