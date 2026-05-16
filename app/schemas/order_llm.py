from pydantic import BaseModel
from typing import List
from app.schemas.order_item_llm import OrderItemLLM

class OrderLLM(BaseModel):
    intent: str
    customer_name: str | None = None
    customer_phone: str | None = None
    delivery_address: str | None = None
    items: List[OrderItemLLM]