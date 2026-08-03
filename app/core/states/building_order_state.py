from sqlalchemy.orm import Session
from app.services.product_resolver_service import resolve_products_from_items
from app.schemas.cart_item_schema import CartItemSchema


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
                "message": "I couldn't add those products",
                "data": {}
            }

        for new_item in resolved_items:

            new_cart_item = CartItemSchema(
                product_id=new_item["product_id"],
                product_name=new_item["product_name"],
                quantity=new_item["quantity"],
                unit_price=new_item["unit_price"],
                subtotal=new_item["unit_price"] * new_item["quantity"]
            )

            found = False

            for cart_item in session.cart_items:

                if cart_item.product_id == new_cart_item.product_id:

                    cart_item.quantity += new_cart_item.quantity
                    cart_item.subtotal = cart_item.unit_price * cart_item.quantity

                    found = True
                    break

            if not found:
                session.cart_items.append(new_cart_item)

        return {
            "type": "message",
            "message": "Done 👍 Would you like anything else or should we review your order?",
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
                "message": "I couldn't find those products in your cart",
                "data": {}
            }

        for remove_item in resolved_items:

            for cart_item in session.cart_items:

                if cart_item.product_id == remove_item["product_id"]:

                    cart_item.quantity -= remove_item["quantity"]

                    if cart_item.quantity <= 0:
                        session.cart_items.remove(cart_item)
                    else:
                        cart_item.subtotal = cart_item.unit_price * cart_item.quantity

                    break

        return {
            "type": "message",
            "message": "Done 👍 I updated your cart",
            "data": {}
        }

    # =========================
    # CLEAR CART
    # =========================
    if intent == "clear_cart":

        session.cart_items = []

        return {
            "type": "message",
            "message": "Cart cleared 👍 What would you like to order?",
            "data": {}
        }

    # =========================
    # REVIEW ORDER TRANSITION
    # =========================
    if intent == "review_order":

        session.current_state = "review_order"

        total = sum(
            item.subtotal for item in session.cart_items
        )

        return {
            "type": "order_summary",
            "message": "Here is your order:",
            "data": {
                "items": [item.model_dump() for item in session.cart_items],
                "total": total
            }
        }

    # =========================
    # DEFAULT
    # =========================
    return {
        "type": "message",
        "message": "I didn't understand 😅 Would you like to add something else or review your order?",
        "data": {}
    }