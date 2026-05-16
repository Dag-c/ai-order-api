from sqlalchemy.orm import Session

from app.core.states.idle_state import (
    handle_idle_state
)

from app.core.states.building_order_state import (
    handle_building_order_state
)

from app.core.states.review_order_state import (
    handle_review_order_state
)

from app.core.states.checkout_state import (
    handle_checkout_state
)


async def handle_chat_state(
    llm_data,
    session,
    db: Session
):

    # =========================
    # IDLE
    # =========================

    if session.current_state == "idle":

        return await handle_idle_state(
            llm_data,
            session,
            db
        )

    # =========================
    # BUILDING ORDER
    # =========================

    if session.current_state == "building_order":

        return await handle_building_order_state(
            llm_data,
            session,
            db
        )

    # =========================
    # REVIEW ORDER
    # =========================

    if session.current_state == "review_order":

        return await handle_review_order_state(
            llm_data,
            session,
            db
        )

    # =========================
    # CHECKOUT
    # =========================

    if session.current_state == "checkout":

        return await handle_checkout_state(
            llm_data,
            session,
            db
        )

    # =========================
    # FALLBACK
    # =========================

    return {
        "type": "message",
        "message": "Estado inválido",
        "data": {}
    }