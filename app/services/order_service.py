from sqlalchemy.orm import Session

from app.schemas.order_schema import OrderCreate
from app.schemas.order_item_schema import OrderItemCreate

from app.repositories.order_repository import create_order, get_orders
from app.repositories.order_item_repository import create_order_items, get_order_items_by_order_id


def create_order_service(
    db: Session,
    session
):
    try:
        # =========================
        # CALCULATE TOTAL
        # =========================

        total_price = sum(
            item["price"] * item["quantity"]
            for item in session.cart_items
        )

        # =========================
        # BUILD ORDER ITEMS
        # =========================

        order_items = []

        for item in session.cart_items:

            subtotal = item["price"] * item["quantity"]

            order_item = OrderItemCreate(

                product_id=item["product_id"],

                quantity=item["quantity"],

                unit_price=item["price"],

                subtotal=subtotal
            )

            order_items.append(order_item)

        # =========================
        # BUILD ORDER SCHEMA
        # =========================

        order_data = OrderCreate(

            customer_name=session.customer_name,

            customer_phone=session.customer_phone,

            delivery_address=session.delivery_address,

            total_price=total_price,

            items=order_items
        )

        # =========================
        # CREATE ORDER
        # =========================

        created_order = create_order(
            db,
            order_data
        )

        # =========================
        # CREATE ORDER ITEMS
        # =========================

        create_order_items(
            db,
            created_order.id,
            order_items
        )

        db.commit()

        # =========================
        # RETURN RESULT
        # =========================

        return {
            "order_id": str(created_order.id),
            "total": total_price,
            "status": created_order.status
        }
    except Exception as e:
        db.rollback()
        raise e

def get_orders_service(db: Session):
    orders = get_orders(db)

    result = []

    for order in orders:

        serialized_items = []

        for item in order.items:

            serialized_items.append({
                "product_id": str(item.product_id),
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "subtotal": float(item.subtotal)
            })

        result.append({
            "id": str(order.id),
            "customer_name": order.customer_name,
            "customer_phone": order.customer_phone,
            "delivery_address": order.delivery_address,
            "status": order.status,
            "total": float(order.total_price),
            "items": serialized_items
        })

    return result