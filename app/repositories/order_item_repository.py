from sqlalchemy.orm import Session

from app.models.order_item import OrderItem
from app.schemas.order_item_schema import OrderItemCreate
from app.models.product_model import Product


def create_order_items(
    db: Session,
    order_id,
    items: list[OrderItemCreate]
):

    created_items = []

    for item in items:

        order_item = OrderItem(

            order_id=order_id,

            product_id=item.product_id,

            quantity=item.quantity,

            unit_price=item.unit_price,

            subtotal=item.subtotal
        )

        db.add(order_item)

        created_items.append(order_item)

    return created_items


def get_order_items_by_order_id(
    db: Session,
    order_id
):
    
    return (
        db.query(
            OrderItem,
            Product.name.label("product_name")
        )
        .join(
            Product,
            Product.id == OrderItem.product_id
        )
        .filter(
            OrderItem.order_id == order_id
        )
        .all()
    )