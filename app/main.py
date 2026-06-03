import os
import logging

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from app.core.database import get_db, engine, Base
from app.core.startup_checks import run_startup_checks
from app.api.api_v1 import api_router
from app.core.redis_listener import redis_listener
from app.core.config import CORS_ORIGINS
from app.core.logging import setup_logging

setup_logging()

run_startup_checks()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("API starting")

    try:
        task = asyncio.create_task(redis_listener())
        logger.info("Redis listener started")

        yield

    finally:
        task.cancel()

    logger.info("API shutting down")

    task.cancel()


app = FastAPI(
    title="AI Order System",
    lifespan=lifespan
)

origins = CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    result = db.execute(select(1))
    return {"status": "ok", "db": result.scalar()}


app.include_router(api_router, prefix="/api/v1")