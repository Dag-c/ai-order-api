from pydantic import BaseModel
from typing import List

from app.schemas.order_item_schema import OrderItemCreate


class OrderCreate(BaseModel):

    customer_name: str

    customer_phone: str

    delivery_address: str

    total_price: float

    items: List[OrderItemCreate]