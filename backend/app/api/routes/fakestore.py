import requests
category = "electronics"

url = f"https://fakestoreapi.com/products/category/{category}"
response = requests.get(url)
data = response.json()
# print(data)


for item in data:
    print(item['title'])
    
