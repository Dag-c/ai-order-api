from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db

from app.schemas.product_schema import ProductCreate, ProductUpdate

from app.services.product_service import (create_product_service, get_products_service, get_product_by_id_service, 
                                          update_product_service, update_product_patch_service, delete_product_service)

from app.core.authenticaion import get_current_user

router = APIRouter()


@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    new_product = create_product_service(db, product)

    return {
        "message": "Product created",
          "product": {
            "id": str(new_product.id),
            "name": new_product.name,
            "description": new_product.description,
            "price":  new_product.price,
            "created_at": new_product.created_at,
            "stock": new_product.stock,
            "is_available": new_product.is_available
        }
    }

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = get_products_service(db)

    return products

@router.get("/{product_id}")
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = get_product_by_id_service(db, product_id)

    return product

@router.put("/{product_id}")
def update_product(product_id: UUID, product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    product_updated = update_product_service(db, product_id, product)

    if not product_updated:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "message": "Product updated",
        "product": {
            "id": str(product_updated.id),
            "name": product_updated.name,
            "description": product_updated.description,
            "price":  product_updated.price,
            "created_at": product_updated.created_at,
            "stock": product_updated.stock,
            "is_available": product_updated.is_available
        }
    }

@router.patch("/{product_id}")
def update_product(product_id: UUID, product: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    product_updated = update_product_patch_service(db, product_id, product)
    
    if not product_updated:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "message": "Product updated",
        "product": {
            "id": str(product_updated.id),
            "name": product_updated.name,
            "description": product_updated.description,
            "price":  product_updated.price,
            "created_at": product_updated.created_at,
            "stock": product_updated.stock,
            "is_available": product_updated.is_available
        }
    }

@router.delete("/{product_id}")
def delete_product(product_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    product = delete_product_service(db, product_id)

    if not product:
        return {
            "message": "Product not found"
        }
    
    return {
        "message": "Product deleted",
        "product": {
            "id": str(product.id),
            "name": product.name
        }
    }
