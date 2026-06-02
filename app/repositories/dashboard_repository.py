from typing import List
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.order_model import Order
from app.models.order_item import OrderItem
from app.models.product_model import Product
from app.enums.order_status import OrderStatus
from app.schemas.dashboard_schema import TopProduct, RecentOrder, SalesByDay

def get_total_orders(db: Session) -> int:

    total = db.query(
        func.count(Order.id)
    ).scalar()

    return total or 0

def get_total_revenue(db: Session) -> float:

    total = db.query(
        func.sum(Order.total_price)
    ).scalar()

    return float(total or 0)

def get_pending_orders(db: Session) -> int:

    total = db.query(
        func.count(Order.id)
    ).filter(
        Order.status == OrderStatus.PENDING
    ).scalar()

    return total or 0

def get_preparing_orders(db: Session) -> int:

    total = db.query(
        func.count(Order.id)
    ).filter(
        Order.status == OrderStatus.PREPARING
    ).scalar()

    return total or 0

def get_delivering_orders(db: Session) -> int:

    total = db.query(
        func.count(Order.id)
    ).filter(
        Order.status == OrderStatus.DELIVERING
    ).scalar()

    return total or 0

def get_top_products(db: Session, limit:int = 5)-> List[TopProduct]:

    result = (
        db.query(
            Product.name.label("product_name"),
            func.sum(OrderItem.quantity).label("total_sold")
        )
        .join(Product, Product.id == OrderItem.product_id)
        .group_by(Product.id, Product.name)
        .order_by(desc("total_sold"))
        .limit(limit)
        .all()
    )

    return result

def get_recent_orders(db: Session, limit:int = 5) -> List[RecentOrder]:

    result= (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .limit(limit)
        .all()
    )

    return result


def get_sales_by_day(db: Session, limit:int = 7) -> List:
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=limit)

    result = (
        db.query(

            func.date(Order.created_at).label("date"),

            func.sum(Order.total_price).label("total")

        )
        .filter(
            Order.created_at >= seven_days_ago
            )
        .group_by(
            func.date(Order.created_at)
        )
        .order_by(
            func.date(Order.created_at)
        )
        .all()
    )

    return result