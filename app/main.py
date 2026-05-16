from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_db, engine, Base
from app.models.product_model import Product
from app.api.api_v1 import api_router

app = FastAPI(title="AI Order System")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    result = db.execute(select(1))
    return {"status": "ok", "db": result.scalar()}

Base.metadata.create_all(bind = engine)
app.include_router(api_router, prefix="/api/v1")