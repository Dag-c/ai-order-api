from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.dashboard_schema import DashboardSummaryResponse

from app.services.dashboard_service import (
    get_total_orders_service, get_total_revenue_service, get_pending_orders_service,
    get_preparing_orders_service, get_delivering_orders_service, get_top_products_service,
    get_recent_orders_service, get_sales_by_day_service
)

from app.core.authenticaion import get_current_user

router = APIRouter()


@router.get("/summary",
            response_model=DashboardSummaryResponse
            )
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return {
        "kpis": {
            "total_orders": get_total_orders_service(db),
            "total_revenue": get_total_revenue_service(db),
            "pending_orders": get_pending_orders_service(db),
            "preparing_orders": get_preparing_orders_service(db),
            "delivering_orders": get_delivering_orders_service(db)
        },

        "top_products": get_top_products_service(db),

        "recent_orders": get_recent_orders_service(db),

        "sales_by_day": get_sales_by_day_service(db)
    }
