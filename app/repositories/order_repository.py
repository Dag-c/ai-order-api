from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from uuid import UUID
from app.models.order_model import Order
from app.models.order_item import OrderItem
from app.schemas.order_schema import OrderCreate



def create_order(
    db: Session,
    order_data: OrderCreate
):

    order = Order(

        customer_name=order_data.customer_name,

        customer_phone=order_data.customer_phone,

        delivery_address=order_data.delivery_address,

        total_price=order_data.total_price,

        status="PENDING"
    )

    db.add(order)
    db.flush()

    return order

def get_orders(db: Session):
    return (
        db.query(Order)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
        .all()
    )

def get_order_by_id(db:Session, order_id: UUID):
    return (db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none())

def update_order_status(db: Session, order_id, new_status: str):

    order = get_order_by_id(db, order_id)

    if not order:
        return None

    order.status = new_status

    db.commit()
    db.refresh(order)

    return order