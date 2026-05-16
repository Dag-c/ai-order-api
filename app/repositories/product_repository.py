from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

def create_product(db: Session, product_data: ProductCreate):

    product =  Product(
        name = product_data.name,
        description = product_data.description,
        price = product_data.price,
        stock = product_data.stock,
        is_available = product_data.is_available
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return product

def get_all_products(db:Session):
    result = db.execute(select(Product))

    return result.scalars().all()


def get_available_products(db):

    products = get_all_products(db)

    return [
        {
            "id": str(p.id),
            "name": p.name,
            "price": float(p.price),
            "available": p.is_available
        }
        for p in products if p.is_available
    ]

def get_product_by_id(db:Session, product_id: UUID):
    result = db.execute(select(Product).where(Product.id == product_id))

    return result.scalar_one_or_none()

def update_product(db:Session, product_id: UUID, product_data: ProductCreate):
    product = db.execute(select(Product).where(Product.id == product_id)).scalar_one_or_none()

    if product:
        product.name = product_data.name
        product.description = product_data.description
        product.price = product_data.price
        product.stock = product_data.stock
        product.is_available = product_data.is_available

        db.commit()

        db.refresh(product)

        return product
    
    return None

def update_product_patch(db: Session, product_id: UUID, product_data: ProductUpdate):
    product = db.execute(select(Product).where(Product.id == product_id)).scalar_one_or_none()

    if not product: 
        return
    
    if product_data.name is not None:
        product.name = product_data.name

    if product_data.description is not None:
        product.description = product_data.description

    if product_data.price is not None:
        product.price = product_data.price

    if product_data.stock is not None:
        product.stock = product_data.stock

    if product_data.is_available is not None:
        product.is_available = product_data.is_available
    
    db.commit()

    db.refresh(product)

    return product

def delete_product(db: Session, product_id: UUID):
    product = db.execute(select(Product).where(Product.id == product_id)).scalar_one_or_none()

    if not product: 
        return None
    
    db.delete(product)
    db.commit()

    return product