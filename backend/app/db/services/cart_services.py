from app.db.models.cart import CartItem
from app.db.db import SessionLocal
from app.db.services.product_service import get_product

user_id = 1


def add_to_cart(product_id: int, quantity: int):
    """Add a proudct to the user cart."""
    product = get_product(product_id)

    if not product:
        return {"error": "product not found"}

    db = SessionLocal()
    try:
        existing_item = (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
            .first()
        )

        if existing_item:
            existing_item.quantity += quantity
            db.commit()

            return {"message": "quantity updated", "cart_item": existing_item}

        item = CartItem(
            user_id=user_id,
            product_id=product_id,
            title=product["title"],
            price=product["price"],
            quantity=quantity,
            image=product["image"],
        )

        db.add(item)
        db.commit()
        db.refresh(item)
    finally:
        db.close()

    return {"message": "Item added to the cart.", "cart_item": item}


def view_cart():
    """View a user's cart."""
    db = SessionLocal()
    items = []
    try:
        items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    finally:
        db.close()

    if not items:
        return {"message": "The cart is empy"}

    total = sum(item.price * item.quantity for item in items)

    return {
        "items": [
            {
                "product_id": item.product_id,
                "title": item.title,
                "price": item.price,
                "quantity": item.quantity,
                "subtotal": item.price * item.quantity,
                "image": item.image,
            }
            for item in items
        ],
        "total": total,
    }


def remove_from_cart(product_id: int):
    """Remove a proudct froma user's cart."""
    db = SessionLocal()
    try:
        item = (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
            .first()
        )

        if not item:
            return {"error": "Item not found"}

        db.delete(item)
        db.commit()
    finally:
        db.close()

    return {"message": "Item removed"}


def update_quantity(product_id: int, quantity: int):
    """Update the quantity of a product in the user's cart."""
    db = SessionLocal()

    try:
        item = (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
            .first()
        )

        if not item:
            return {"error": "Item not found"}

        item.quantity = quantity

        db.commit()
    finally:
        db.close()

    return {"message": "Quantity updated"}


def clear_cart():
    """Remove all the products from the cart."""
    db = SessionLocal()

    try:
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()

        db.commit()
    finally:
        db.close()

    return {"message": "Cart cleared"}
