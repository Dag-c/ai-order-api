from fastapi import FastAPI
from app.api.api_v1 import api_router

app = FastAPI(title="AI Order System")

app.include_router(api_router, prefix="/api/v1")