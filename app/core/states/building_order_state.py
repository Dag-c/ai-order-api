from sqlalchemy.orm import Session

from app.services.product_resolver_service import (
    resolve_products_from_items
)


async def handle_building_order_state(
    llm_data,
    session,
    db: Session
):

    intent = llm_data.intent
    data = llm_data.data or {}

    # =========================
    # ADD TO CART
    # =========================

    if intent == "add_to_cart":

        raw_items = data.get("items", [])

        resolved_items = resolve_products_from_items(
            db,
            raw_items
        )

        if not resolved_items:

            return {
                "type": "message",
                "message": "No pude agregar esos productos",
                "data": {}
            }

        # =====================================
        # MERGE QUANTITIES
        # =====================================

        for new_item in resolved_items:

            found = False

            for cart_item in session.cart_items:

                if (
                    cart_item["product_id"]
                    == new_item["product_id"]
                ):

                    cart_item["quantity"] += (
                        new_item["quantity"]
                    )

                    found = True
                    break

            if not found:

                session.cart_items.append(
                    new_item
                )

        return {
            "type": "message",
            "message": (
                "Listo 👍 "
                "¿Quieres algo más o revisamos tu orden?"
            ),
            "data": {}
        }

    # =========================
    # REMOVE FROM CART
    # =========================

    if intent == "remove_from_cart":

        raw_items = data.get("items", [])

        resolved_items = resolve_products_from_items(
            db,
            raw_items
        )

        if not resolved_items:

            return {
                "type": "message",
                "message": (
                    "No encontré esos productos "
                    "en tu carrito"
                ),
                "data": {}
            }

        # =====================================
        # SUBTRACT QUANTITIES
        # =====================================

        for remove_item in resolved_items:

            for cart_item in session.cart_items:

                if (
                    cart_item["product_id"]
                    == remove_item["product_id"]
                ):

                    cart_item["quantity"] -= (
                        remove_item["quantity"]
                    )

                    # REMOVE IF EMPTY

                    if (
                        cart_item["quantity"]
                        <= 0
                    ):

                        session.cart_items.remove(
                            cart_item
                        )

                    break

        return {
            "type": "message",
            "message": (
                "Listo 👍 "
                "actualicé tu carrito"
            ),
            "data": {}
        }

    # =========================
    # CLEAR CART
    # =========================

    if intent == "clear_cart":

        session.cart_items = []

        return {
            "type": "message",
            "message": (
                "Carrito vaciado 👍 "
                "¿Qué te gustaría ordenar?"
            ),
            "data": {}
        }

    # =========================
    # REVIEW ORDER
    # TRANSITION
    # =========================

    if intent == "review_order":

        session.current_state = (
            "review_order"
        )

        total = sum(
            item["price"] * item["quantity"]
            for item in session.cart_items
        )

        return {
            "type": "order_summary",
            "message": "Este es tu pedido:",
            "data": {
                "items": session.cart_items,
                "total": total
            }
        }

    # =========================
    # DEFAULT
    # =========================

    return {
        "type": "message",
        "message": (
            "No entendí 😅 "
            "¿quieres agregar algo más "
            "o revisar tu pedido?"
        ),
        "data": {}
    }