from app.agenticAI.schema.schema import Product
from typing import Any
import requests
import math


base_url = "https://fakestoreapi.com"


# FakeStoreAPI Tools

def fetch_all_products() -> list[Product]:
    """Fetch every product from FakeStoreAPI."""
    res = requests.get(f"{base_url}/products")
    return [Product(**p) for p in res.json()]

def fetch_products_by_category(category: str = None) -> list[Product] | None:
    """Fetch products belonging to a specific category."""
    res = requests.get(f"{base_url}/products/category/{category}")
    res = res.json()
    if len(res) == 0:
        return None
    return [Product(**p) for p in res]

def fetch_product_by_id(product_id: int = None) -> Product | None:
    """Fetch a single product by its ID"""
    res = requests.get(f"{base_url}/products/{product_id}")
    if res.status_code == 404:
        return None
    return Product(**res.json())

def fetch_categories() -> list[str]:
    """Fetch all available product categories."""
    res = requests.get(f"{base_url}/categories")
    return res.json()



def search_products(query: str = "",category: str | None = None,min_price: float | None = None,max_price: float | None = None):

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

    return res


# Analytics Tools

def score_product(p: Product,price_weight: float = 0.5,rating_weight: float = 0.3,popularity_weight: float = 0.2,max_price: float | None = None):
    """Score a product on a 0-100 scale using weighted criteria."""

    if max_price is None or max_price <= 0:
        max_price = p.price if p.price > 0 else 1.0

    price_score = max(0,(1 - p.price/max_price))*100
    rating_score = (p.rating.rate/5.0)*100
    popularity_score = min(100 , (math.log1p(p.rating.count)/math.log1p(100))*100)

    overall_score = (
        price_weight*price_score + rating_weight*rating_score + popularity_weight*popularity_score
    )
    return {
        "product_id":p.id,
        "title":p.title,
        "price":p.price,
        "rating":p.rating.rate,
        "review_count":p.rating.count,
        "overall_score": round(overall_score,1)
    }

def compare_products(products: list[Product],max_price: float | None = None):
    """Generate a comparison of multiple products."""
    if not products:
        return {"error": "No products to compare."}
    if max_price is None:
        max_price = max(p.price for p in products)
    max_price *= 1.1

    # sort product according to their scores.
    scores = [score_product(p,max_price = max_price) for p in products ]
    scores.sort(key = lambda s: s['overall_score'], reverse = True)

    trade_offs: list[str] = []
    # compare every pair of product in the products list 
    for i in range(len(scores)):
        for j in range(i+1,len(scores)):
            p1 , p2 = scores[i] , scores[j]

            price_diff = abs(p1['price'] - p2['price'])
            rating_diff = abs(p1['rating'] - p2['rating'])

            cheaper = p1['title'] if p1['price'] > p2['price'] else p2['title']
            better_rated = p1['title'] if p1['rating'] > p2['rating'] else p2['title']

            trade_offs.append(
                f"{cheaper} is {price_diff} cheaper."
                f"{better_rated} has {rating_diff} higher rating."
            )
    best = scores[0]

    return {
        "comparison": [
            {
                'product_id': s['product_id'],
                'title': s['title'],
                'price': s['price'],
                'rating': s['rating'],
                'review_count': s['review_count'],
                'score': s['overall_score'],
            }
            for s in scores
        ],
        "trade_offs": trade_offs,
        "recommendation": {
            "product_id": best['product_id'],
            "title": best['title'],
            "score": best['overall_score'],
            'reason': (
                f"{best['title'] } scores highest overall ({best['overall_score']}/100) with the best balance of price,rating and popularity."
            )
        }
    }


def rank_products(products: list[Product],price_weight: float = 0.5,rating_weight: float = 0.3,popularity_weight: float = 0.2) -> list[dict[str, Any]]:
    """Rank a list of products by weighted score (Highest first)."""

    # max_price + 10 % : used to calculate price_score while scoring a product.
    max_price = max(p.price for p in products) * 1.1

    scored = [
        score_product(p,price_weight,rating_weight,popularity_weight,max_price)
        for p in products
    ]
    scored.sort(key = lambda s: s['overall_score'], reverse = True)
    for rank,s in enumerate(scored,1):
        s["rank"] = rank
    return scored


# test
# print(fetch_product_by_id(1))
# print(fetch_all_products())
# print(fetch_categories()) 
# print(rank_prodcuts(fetch_products_by_category('electronics')))
# print(compare_products(fetch_products_by_category('jewelery')))