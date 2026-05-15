import requests

BASE_URL = "https://fakestoreapi.com/products"


def get_product(product_id: int):
    """Get product by ID"""
    response = requests.get(f"{BASE_URL}/{product_id}")

    if response.status_code != 200:
        return None
    return response.json()
