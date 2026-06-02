from sqlalchemy.orm import Session

from app.services.order_service import create_order_service

from app.core.events import publish_order_event


async def handle_checkout_state(
    llm_data,
    session,
    db: Session
):
    data = llm_data.data or {}

    # =========================
    # SAVE CUSTOMER DATA
    # =========================

    if data.get("customer_name"):
        session.customer_name = data["customer_name"]

    if data.get("customer_phone"):
        session.customer_phone = data["customer_phone"]

    if data.get("delivery_address"):
        session.delivery_address = data["delivery_address"]

    # =========================
    # VALIDATE REQUIRED DATA
    # =========================

    missing_fields = []

    if not session.customer_name:
        missing_fields.append("nombre")

    if not session.customer_phone:
        missing_fields.append("teléfono")

    if not session.delivery_address:
        missing_fields.append("dirección")

    if missing_fields:
        return {
            "type": "checkout_form",
            "message": "Para continuar necesito: " + ", ".join(missing_fields),
            "data": {}
        }

    # =========================
    # VALIDATE CART (IMPORTANTE)
    # =========================

    if not session.cart_items:
        return {
            "type": "message",
            "message": "Tu carrito está vacío",
            "data": {}
        }

    # =========================
    # CREATE ORDER
    # =========================

    created_order = create_order_service(db, session)
    publish_order_event(
        event_type="order_created",
        data=created_order.model_dump(mode="json")
    )

    # =========================
    # RESET SESSION
    # =========================

    session.current_state = "idle"
    session.cart_items = []

    session.customer_name = None
    session.customer_phone = None
    session.delivery_address = None

    # =========================
    # RESPONSE
    # =========================

    return {
        "type": "order_created",
        "message": "Tu orden fue creada correctamente",
        "data": {
            "order_id": created_order.id,
            "total": created_order.total,
            "status": created_order.status
        }
    }