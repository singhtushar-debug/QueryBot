from app.agenticAI.schema.schema import Product
from langchain_core.tools import tool
from app.db.services.cart_services import (
    add_to_cart,
    remove_from_cart,
    update_quantity,
    clear_cart,
    view_cart,
)
from typing import Any
import requests
import math
import json

base_url = "https://fakestoreapi.com"


# FakeStoreAPI Tools


# @tool
def fetch_all_products() -> list[Product]:
    """Fetch every product from FakeStoreAPI."""
    res = requests.get(f"{base_url}/products")
    return [Product(**p) for p in res.json()]


# @tool
def fetch_products_by_category(category: str = None) -> list[Product] | None:
    """Fetch products belonging to a specific category."""
    res = requests.get(f"{base_url}/products/category/{category}")
    res = res.json()
    if len(res) == 0:
        return None
    return [Product(**p) for p in res]


@tool
def fetch_product_by_id(product_id: int = None) -> str:
    """
        Fetch a single product by its ID.
        
        Args:
            proudct_id: int => id for the product.
    """
    res = requests.get(f"{base_url}/products/{product_id}")
    if res.status_code == 404:
        return None
    return res.json()


@tool
def fetch_categories() -> list[str]:
    """ 
        Fetch all available product categories.
    """
    res = requests.get(f"{base_url}/products/categories")
    return res.json()


@tool
def search_products(
    query: str = "",
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
):
    """
        Search products in the inventory.

        Args:
            query: str => original user query (must be a string).
            category: str | None => category in which the product belongs.
            min_price: float | None => minimum price limit.
            max_price: float | None => maximum price limit.
    """

    if category:
        products = fetch_products_by_category(category)
    else:
        products = fetch_all_products()

    res = products

    if min_price is not None:
        res = [p for p in res if p.price >= min_price]

    if max_price is not None:
        res = [p for p in res if p.price <= max_price]

    if query:
        """Search keywords from query for advance filtering"""

    clean_products = []
    for p in res:
        # Convert to dict
        product_dict = p.model_dump()

        # TRUNCATE DESCRIPTION: Keep only the first 500 characters
        if product_dict.get("description"):
            product_dict["description"] = product_dict["description"][:500] + "..."

        clean_products.append(product_dict)

    return json.dumps(clean_products)


# Analytics Tools


def score_product(
    p: Product,
    price_weight: float = 0.5,
    rating_weight: float = 0.3,
    popularity_weight: float = 0.2,
    max_price: float | None = None,
):
    """
        Score a product on a 0-100 scale using weighted criteria.

        Args:
            p: Product => Product.
            max_price: float | None => maximum price limit.
    """

    if max_price is None or max_price <= 0:
        max_price = p.price if p.price > 0 else 1.0

    price_score = max(0, (1 - p.price / max_price)) * 100
    rating_score = (p.rating.rate / 5.0) * 100
    popularity_score = min(100, (math.log1p(p.rating.count) / math.log1p(100)) * 100)

    overall_score = (
        price_weight * price_score
        + rating_weight * rating_score
        + popularity_weight * popularity_score
    )
    return {
        "product_id": p.id,
        "title": p.title,
        "price": p.price,
        "rating": p.rating.rate,
        "review_count": p.rating.count,
        "overall_score": round(overall_score, 1),
    }


@tool
def rank_products(
    products: str,
    price_weight: float = 0.5,
    rating_weight: float = 0.3,
    popularity_weight: float = 0.2,
) -> list[dict[str, Any]]:
    """Rank a list of products by weighted score (Highest first)."""
    try:
        data = json.loads(products)
        # Re-instantiate as Product objects so your score_product function works
        products = [Product(**p) for p in data]
    except Exception as e:
        return f"Error parsing product list: {str(e)}"

    if not products:
        return "No products found to rank."

    # max_price + 10 % : used to calculate price_score while scoring a product.
    max_price = max(p.price for p in products) * 1.1

    scored = [
        score_product(p, price_weight, rating_weight, popularity_weight, max_price)
        for p in products
    ]
    scored.sort(key=lambda s: s["overall_score"], reverse=True)
    for rank, s in enumerate(scored, 1):
        s["rank"] = rank
    return json.dumps(scored)


# Cart related tools


@tool
def add_to_cart_tool(product_id: int, quantity: int = 1):
    """
    Add product to cart.

    product_id must be integer.
    quantity must be integer.
    Never pass strings.
    """

    return add_to_cart(product_id, quantity)


@tool
def view_cart_tool():
    """View all items in cart."""

    return view_cart()


@tool
def remove_from_cart_tool(product_id: int):
    """
        Remove proudct from cart.

        product_id must be integer.
    """

    return remove_from_cart(product_id)


@tool
def update_quantity_tool(product_id: int, quantity: int):
    """ 
        Update the quantity of a product.

        product_id must be integer.
        quantity must be integer.
    """

    return update_quantity(product_id, quantity)


@tool
def clear_cart_tool():
    """Remove all items from cart"""
    return clear_cart()
