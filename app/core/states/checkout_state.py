from sqlalchemy.orm import Session

from app.services.order_service import (
    create_order_service
)


async def handle_checkout_state(
    llm_data,
    session,
    db: Session
):

    data = llm_data.data or {}

    # =====================================
    # SAVE CUSTOMER DATA
    # =====================================

    customer_name = data.get("customer_name")
    customer_phone = data.get("customer_phone")
    delivery_address = data.get("delivery_address")

    if customer_name:
        session.customer_name = customer_name

    if customer_phone:
        session.customer_phone = customer_phone

    if delivery_address:
        session.delivery_address = delivery_address

    # =====================================
    # VALIDATE REQUIRED DATA
    # =====================================

    missing_fields = []

    if not session.customer_name:
        missing_fields.append("nombre")

    if not session.customer_phone:
        missing_fields.append("telefono")

    if not session.delivery_address:
        missing_fields.append("direccion")

    # =====================================
    # ASK MISSING DATA
    # =====================================

    if missing_fields:

        return {
            "type": "checkout_form",
            "message": (
                "Para continuar necesito tu: "
                + ", ".join(missing_fields)
            ),
            "data": {}
        }

    # =====================================
    # CREATE ORDER
    # =====================================

    created_order = create_order_service(
        db,
        session
    )

    # =====================================
    # RESET SESSION
    # =====================================

    session.current_state = "idle"

    session.cart_items = []

    session.customer_name = None
    session.customer_phone = None
    session.delivery_address = None

    # =====================================
    # SUCCESS RESPONSE
    # =====================================

    return {
        "type": "order_created",
        "message": "Tu orden fue creada correctamente",
        "data": {
            "order_id": created_order["order_id"],
            "total": created_order["total"],
            "status": created_order["status"]
        }
    }