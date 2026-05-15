import requests

category = "electronics"

url = "https://fakestoreapi.com/products/categories"
response = requests.get(url)
data = response.json()
print(data)
# print(data)


# for item in data:
#     print(item)
