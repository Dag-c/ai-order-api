from sqlalchemy.orm import Session
from app.core.states.building_order_state import handle_building_order_state


async def handle_review_order_state(
    llm_data,
    session,
    db: Session
):

    intent = llm_data.intent

    # =========================
    # REVIEW ORDER
    # =========================
    if intent == "review_order":

        total = sum(
            item.subtotal for item in session.cart_items
        )

        return {
            "type": "order_summary",
            "message": "Este es tu pedido:",
            "data": {
                "items": [
                    item.model_dump()
                    for item in session.cart_items
                ],
                "total": total
            }
        }

    # =========================
    # BACK TO BUILDING ORDER
    # ADD PRODUCTS
    # =========================
    if intent == "add_to_cart":

        session.current_state = "building_order"

        return await handle_building_order_state(
            llm_data,
            session,
            db
        )

    # =========================
    # BACK TO BUILDING ORDER
    # REMOVE PRODUCTS
    # =========================
    if intent == "remove_from_cart":

        session.current_state = "building_order"

        return await handle_building_order_state(
            llm_data,
            session,
            db
        )

    # =========================
    # CHECKOUT TRANSITION
    # =========================
    if intent == "checkout":

        if not session.cart_items:

            return {
                "type": "message",
                "message": (
                    "Tu carrito está vacío 👍 "
                    "Primero agrega algunos productos"
                ),
                "data": {}
            }

        session.current_state = "checkout"

        return {
            "type": "checkout_form",
            "message": (
                "Perfecto 👍 "
                "Ahora necesito tu nombre, "
                "teléfono y dirección"
            ),
            "data": {}
        }

    # =========================
    # DEFAULT
    # =========================
    return {
        "type": "message",
        "message": (
            "No entendí 😅 "
            "¿quieres confirmar tu pedido o modificar algo?"
        ),
        "data": {}
    }