from sqlalchemy.orm import Session

from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.repositories.product_repository import (create_product, get_all_products, get_available_products,get_product_by_id, 
                                                 update_product, update_product_patch, delete_product)
from uuid import UUID

def create_product_service(db: Session, product_data:ProductCreate):
    return create_product(db, product_data)

def get_products_service(db: Session):
    return get_all_products(db)

async def get_available_products_service(db):
    return get_available_products(db)

def get_product_by_id_service(db: Session, product_id: UUID):
    return get_product_by_id(db, product_id)

def update_product_service(db: Session, product_id: UUID, product_data: ProductCreate):
    return update_product(db, product_id, product_data)

def update_product_patch_service(db: Session, product_id: UUID, product_data: ProductUpdate):
    return update_product_patch(db, product_id, product_data)

def delete_product_service(db: Session, product_id: UUID):
    return delete_product(db, product_id)
