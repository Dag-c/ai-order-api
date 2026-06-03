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
            continue

        unit_price = float(product.price)

        resolved_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": unit_price * quantity
        })

    return resolved_items