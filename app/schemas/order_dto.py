from pydantic import BaseModel
from uuid import UUID
from typing import List
from app.schemas.order_item_dto import OrderItemDTO


class OrderDTO(BaseModel):
    id: UUID
    customer_name: str
    customer_phone: str
    delivery_address: str
    status: str
    total: float
    items: List[OrderItemDTO]