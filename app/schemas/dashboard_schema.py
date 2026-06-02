from pydantic import BaseModel

class DashboardKPI(BaseModel):
    total_orders: int
    total_revenue: float

    pending_orders: int
    preparing_orders: int
    delivering_orders: int

class TopProduct(BaseModel):
    product_name: str
    total_sold: int

class RecentOrder(BaseModel):
    order_id: str

    customer_name: str

    status: str

    total_price: float

class SalesByDay(BaseModel):
    date: str
    total: float

class DashboardSummaryResponse(BaseModel):

    kpis: DashboardKPI

    top_products: list[TopProduct]

    recent_orders: list[RecentOrder]

    sales_by_day: list[SalesByDay]
