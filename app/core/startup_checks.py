import redis
import logging
from sqlalchemy import text

from app.core.database import engine
from app.core.config import REDIS_URL

logger = logging.getLogger(__name__)

def validate_database():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        logger.info("Database connected")

    except Exception as e:

        logger.error(
            "Database connection failed: %s",
            e
        )

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

        logger.info("Redis connected")

    except Exception as e:

        logger.exception(
            "Redis connection failed: %s",
            e
        )

        raise RuntimeError(
            f"Redis connection failed: {e}"
        )


def run_startup_checks():

    logger.info("Running startup checks")

    validate_database()

    validate_redis()

    logger.info("All startup checks passed")