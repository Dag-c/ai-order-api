from sqlalchemy import Column, String, Numeric, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
import uuid

from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    
    description = Column(String)

    price = Column(Numeric(10, 2), nullable=False)

    stock = Column(Integer, default=0)
    
    is_available = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())