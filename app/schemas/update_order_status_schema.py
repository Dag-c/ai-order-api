from pydantic import BaseModel
from app.enums.order_status import OrderStatus

class UpdateOrderStatusSchema(BaseModel):
    status: OrderStatus