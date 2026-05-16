from pydantic import BaseModel, Field
from typing import List, Optional

from app.schemas.order_item_llm import OrderItemLLM


class ChatSessionSchema(BaseModel):

    current_state: str = "idle"

    cart_items: List[OrderItemLLM] = Field(default_factory=list)

    customer_name: Optional[str] = None

    customer_phone: Optional[str] = None

    delivery_address: Optional[str] = None