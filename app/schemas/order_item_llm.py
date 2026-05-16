from pydantic import BaseModel

class OrderItemLLM(BaseModel):
    product: str
    quantity: int