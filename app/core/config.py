import os
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

# =========================
# HELPERS
# =========================

def required_env(key: str) -> str:
    """
    Get required environment variable.
    Crash app if missing.
    """

    value = os.getenv(key)

    if value is None or value.strip() == "":
        raise RuntimeError(
            f"Missing required environment variable: {key}"
        )

    return value


# =========================
# APP ENV
# =========================

ENV = os.getenv("ENV", "development")

# =========================
# DATABASE
# =========================

DB_USER = required_env("DB_USER")

DB_PASSWORD = required_env("DB_PASSWORD")

DB_HOST = required_env("DB_HOST")

DB_PORT = int(
    os.getenv("DB_PORT", 5432)
)

DB_NAME = required_env("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?sslmode=require"
)

# =========================
# GEMINI
# =========================

GEMINI_API_KEY = required_env(
    "GEMINI_API_KEY"
)

# =========================
# AUTH
# =========================

SECRET_APP_KEY = required_env(
    "SECRET_APP_KEY"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

# =========================
# REDIS
# =========================

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379"
)

SESSION_TTL_SECONDS = int(
    os.getenv(
        "SESSION_TTL_SECONDS",
        3600
    )
)

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")