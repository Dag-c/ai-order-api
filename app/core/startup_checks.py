import redis
from sqlalchemy import text

from app.core.database import engine
from app.core.config import REDIS_URL


def validate_database():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        print(" Database connected")

    except Exception as e:

        raise RuntimeError(
            f"Database connection failed: {e}"
        )


def validate_redis():

    try:

        client = redis.from_url(
            REDIS_URL,
            decode_responses=True
        )

        client.ping()

        print(" Redis connected")

    except Exception as e:

        raise RuntimeError(
            f"Redis connection failed: {e}"
        )


def run_startup_checks():

    print(" Running startup checks...")

    validate_database()

    validate_redis()

    print(" All startup checks passed")