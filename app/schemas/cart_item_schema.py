from pydantic import BaseModel
from uuid import UUID


class CartItemSchema(BaseModel):
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float