from pydantic import BaseModel, Field
from typing import List, Optional

from app.schemas.cart_item_schema import CartItemSchema


class ChatSessionSchema(BaseModel):

    current_state: str = "idle"

    cart_items: List[CartItemSchema] = Field(default_factory=list)

    customer_name: Optional[str] = None

    customer_phone: Optional[str] = None

    delivery_address: Optional[str] = None