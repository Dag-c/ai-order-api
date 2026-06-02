from sqlalchemy import select, and_
from datetime import datetime, date, time
from zoneinfo import ZoneInfo

from app.models.order_model import Order


class OrderQueryBuilder:
    MEXICO_TZ = ZoneInfo("America/Mexico_City")
    UTC = ZoneInfo("UTC")

    def __init__(self):
        self.query = select(Order).options()

    def apply_date_filters(self, filters):

        if filters.today:
            #  1. HOY EN GUADALAJARA
            now_local = datetime.now(self.MEXICO_TZ)
            today_local = now_local.date()

            #  2. RANGO LOCAL (00:00 - 23:59)
            start_local = datetime.combine(today_local, time.min, tzinfo=self.MEXICO_TZ)
            end_local = datetime.combine(today_local, time.max, tzinfo=self.MEXICO_TZ)

            #  3. CONVERTIR A UTC (lo que usa la DB)
            start_utc = start_local.astimezone(self.UTC)
            end_utc = end_local.astimezone(self.UTC)

            print("hoy MX:", today_local)
            print("start UTC:", start_utc)
            print("end UTC:", end_utc)

            self.query = self.query.where(
                and_(
                    Order.created_at >= start_utc,
                    Order.created_at <= end_utc
                )
            )

        elif filters.from_date and filters.to_date:

            # IMPORTANTE: también debes asumir que estos vienen en MX
            start_local = datetime.combine(filters.from_date, time.min, tzinfo=self.MEXICO_TZ)
            end_local = datetime.combine(filters.to_date, time.max, tzinfo=self.MEXICO_TZ)

            start_utc = start_local.astimezone(self.UTC)
            end_utc = end_local.astimezone(self.UTC)

            self.query = self.query.where(
                and_(
                    Order.created_at >= start_utc,
                    Order.created_at <= end_utc
                )
            )

        return self

    def apply_status(self, filters):
        if filters.status:
            self.query = self.query.where(Order.status == filters.status)
        return self

    def build(self):
        return self.query