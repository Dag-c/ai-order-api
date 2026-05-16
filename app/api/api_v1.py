from fastapi import APIRouter
from app.api.routers import orders, products, users, chat, auth

api_router = APIRouter()

api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(auth.router, prefix="/login", tags=["Login"])