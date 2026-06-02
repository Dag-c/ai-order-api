from typing import List

from app.schemas.dashboard_schema import TopProduct, SalesByDay
from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import (
    get_total_orders, get_total_revenue, get_pending_orders,
    get_preparing_orders, get_delivering_orders, get_top_products,
    get_recent_orders, get_sales_by_day
)

def get_total_orders_service(
        db: Session
        ) -> int: 
    return get_total_orders(db)

def get_total_revenue_service(db: Session) -> float:
    return get_total_revenue(db)

def get_pending_orders_service(db: Session) -> int:
    return get_pending_orders(db)

def get_preparing_orders_service(db: Session) -> int:
    return get_preparing_orders(db)

def get_delivering_orders_service(db: Session) -> int:
    return get_delivering_orders(db)

def get_top_products_service(db: Session) -> List[TopProduct]:
    
    rows = get_top_products(db)

    return [
        {
            "product_name": name,
            "total_sold": total
        }
        for name, total in rows
    ]

def get_recent_orders_service(db: Session):

    orders = get_recent_orders(db)

    return [
        {
            "order_id": str(order.id),
            "customer_name": order.customer_name,
            "status": order.status,
            "total_price": float(order.total_price),
            "created_at": order.created_at.isoformat()
        }
        for order in orders
    ]

def get_sales_by_day_service(
        db: Session
    ) -> List[SalesByDay]:

    rows = get_sales_by_day(db)

    return [
        {
            "date": str(r.date),
            "total": r.total
        }
        for r in rows
    ]