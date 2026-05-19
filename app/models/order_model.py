from sqlalchemy import Column, String, Numeric, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.order_item import OrderItem
import uuid

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    customer_name = Column(String(255), nullable=True)
    customer_phone = Column(String(50), nullable=True)
    delivery_address = Column(String, nullable=True)

    status = Column(String(50), nullable=False, default="PENDING")

    total_price = Column(Numeric(10, 2), default=0)

    created_at = Column(TIMESTAMP, server_default=func.now())

    items = relationship("OrderItem", backref="order", lazy="selectin")

