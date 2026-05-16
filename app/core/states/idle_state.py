from sqlalchemy.orm import Session

from app.services.product_service import (
    get_available_products_service
)

from app.services.product_resolver_service import (
    resolve_products_from_items
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
            "message": "Hola, bienvenido. ¿Qué te gustaría ordenar?",
            "data": {}
        }

    # =========================
    # ASK MENU
    # =========================
    if intent == "ask_menu":

        products = await get_available_products_service(db)

        return {
            "type": "menu",
            "message": "Estos son los platillos disponibles",
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
                "message": "No encontré ese producto",
                "data": {}
            }

        available_products = [
            item["product_name"]
            for item in resolved_items
        ]

        return {
            "type": "availability",
            "message": "Sí tenemos disponible:",
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
                "message": "No pude agregar productos",
                "data": {}
            }

        # TRANSITION
        session.current_state = "building_order"

        session.cart_items.extend(resolved_items)

        return {
            "type": "message",
            "message": "Agregado al carrito. ¿Deseas algo más?",
            "data": {}
        }

    # =========================
    # UNKNOWN
    # =========================
    return {
        "type": "message",
        "message": "No entendí tu solicitud",
        "data": {}
    }