import redis

from app.schemas.chat_session_schema import ChatSessionSchema
from app.core.config import REDIS_URL, SESSION_TTL_SECONDS

redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True
)

def get_session(session_id: str) -> ChatSessionSchema:
    data = redis_client.get(session_id)

    if data is None:
        session = ChatSessionSchema()
        save_session(session_id, session)
        return session

    return ChatSessionSchema.model_validate_json(data)


def save_session(session_id: str, session: ChatSessionSchema):
    redis_client.setex(
        session_id,
        SESSION_TTL_SECONDS,
        session.model_dump_json()
    )