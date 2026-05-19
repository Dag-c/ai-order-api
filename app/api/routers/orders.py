from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.services.order_service import get_orders_service
from app.schemas.update_order_status_schema import UpdateOrderStatusSchema
from app.repositories.order_repository import update_order_status
from app.core.authenticaion import get_current_user

router = APIRouter()

@router.get("/")
def get_orders_endpoint(db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    return get_orders_service(db)

@router.post("/")
def create_order():
    return {"message": "order created"}

@router.patch("/orders/{order_id}/status")
def change_order_status(
    order_id: UUID,
    payload: UpdateOrderStatusSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    updated = update_order_status(db, order_id, payload.status)

    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "message": "Status updated",
        "order": {
            "id": str(updated.id),
            "status": updated.status
        }
    }