from sqlalchemy.orm import Session
from config import RESTAURANT_NAME

from app.services.product_service import (
    get_available_products_service
)

from app.services.product_resolver_service import (
    resolve_products_from_items
)

from app.schemas.cart_item_schema import (
    CartItemSchema
)


async def handle_idle_state(
    data,
    session,
    db: Session
):

    intent = data.intent
    data = data.data or {}

    # =========================
    # GREETING
    # =========================

    if intent == "greeting":

        return {
            "type": "message",
            "message": (
                f"Welcome to {RESTAURANT_NAME}! 🌮 What would you like to order today?"
            ),
            "data": {}
        }

    # =========================
    # ASK MENU
    # =========================

    if intent == "ask_menu":

        products = await get_available_products_service(db)

        return {
            "type": "menu",
            "message": (
                "Here are today's available dishes"
            ),
            "data": {
                "products": products
            }
        }

    # =========================
    # ASK AVAILABILITY
    # =========================

    if intent == "ask_availability":

        raw_items = data.get("items", [])

        resolved_items = resolve_products_from_items(
            db,
            raw_items
        )

        if not resolved_items:

            return {
                "type": "message",
                "message": (
                    "I couldn't find that product"
                ),
                "data": {}
            }

        available_products = [
            item["product_name"]
            for item in resolved_items
        ]

        return {
            "type": "availability",
            "message": (
                "We have these products available:"
            ),
            "data": {
                "products": available_products
            }
        }

    # =========================
    # ADD TO CART
    # TRANSITION → BUILDING_ORDER
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
                "message": (
                    "I couldn't add those products"
                ),
                "data": {}
            }

        # =========================
        # TRANSITION
        # =========================

        session.current_state = (
            "building_order"
        )

        # =========================
        # CONVERT DICTS TO SCHEMA
        # =========================

        session.cart_items.extend(
            [
                CartItemSchema(**item)
                for item in resolved_items
            ]
        )

        return {
            "type": "message",
            "message": (
                "Added to your cart 👍 "
                "Would you like anything else?"
            ),
            "data": {}
        }

    # =========================
    # UNKNOWN
    # =========================

    return {
        "type": "message",
        "message": (
            "I didn't understand your request"
        ),
        "data": {}
    }