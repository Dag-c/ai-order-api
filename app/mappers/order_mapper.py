from app.schemas.order_dto import OrderDTO, OrderItemDTO


def map_order_to_dto(order) -> OrderDTO:

    return OrderDTO(
        id=str(order.id),
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        delivery_address=order.delivery_address,
        status=order.status,
        total=float(order.total_price),

        items=[
            OrderItemDTO(
                product_id=str(item.product_id),

                product_name=(
                    item.product.name
                    if item.product and item.product.name
                    else "Unknown Product"
                ),

                quantity=item.quantity,
                unit_price=float(item.unit_price),
                subtotal=float(item.subtotal),
            )
            for item in order.items
        ],
    )