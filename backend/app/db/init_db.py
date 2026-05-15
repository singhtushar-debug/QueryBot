from app.db.db import engine
from app.db.models.cart import CartItem


def init_database():
    """Create tables"""
    CartItem.metadata.create_all(bind=engine)


print("Tables created")
