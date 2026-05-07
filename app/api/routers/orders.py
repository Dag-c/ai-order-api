from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_orders():
    return {"message": "list of orders"}

@router.post("/")
def create_order():
    return {"message": "order created"}