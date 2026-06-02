from sqlalchemy.orm import Session

from app.repositories.order_repository import (
    create_order,
    get_orders
)

from app.repositories.order_item_repository import (
    create_order_items
)

from app.schemas.order_schema import OrderCreate
from app.schemas.order_item_schema import OrderItemCreate

from app.mappers.order_mapper import map_order_to_dto


# =========================
# CREATE ORDER
# =========================
def create_order_service(db: Session, session):

    try:
        total_price = sum(
            item.subtotal for item in session.cart_items
        )

        order_items = []

        for item in session.cart_items:
            order_items.append(
                OrderItemCreate(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal
                )
            )

        order_data = OrderCreate(
            customer_name=session.customer_name,
            customer_phone=session.customer_phone,
            delivery_address=session.delivery_address,
            total_price=total_price,
            items=order_items
        )

        created_order = create_order(db, order_data)

        create_order_items(
            db,
            created_order.id,
            order_items
        )

        db.commit()

        #  SINGLE SOURCE OF TRUTH OUTPUT
        return map_order_to_dto(created_order)

    except Exception as e:
        db.rollback()
        raise e


# =========================
# GET ALL ORDERS
# =========================
def get_orders_service(db: Session, filters=None):

    orders = get_orders(db, filters)

    return [map_order_to_dto(o) for o in orders]