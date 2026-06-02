from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class OrderFilters(BaseModel):
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    today: bool = False
    status: Optional[str] = None