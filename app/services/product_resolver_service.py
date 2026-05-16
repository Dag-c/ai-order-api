from sqlalchemy.orm import Session
from app.models.product_model import Product


def resolve_products_from_items(db: Session, items: list):

    resolved_items = []

    for item in items:

        name = item["product"]
        quantity = item["quantity"]

        product = db.query(Product).filter(
            Product.name.ilike(f"%{name}%")
        ).first()

        if not product:
            continue  # o marcar error después

        resolved_items.append({
            "product_id": str(product.id),
            "product_name": product.name,
            "quantity": quantity,
            "price": float(product.price)
        })

    return resolved_items