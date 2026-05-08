import requests

url = "https://fakestoreapi.com/products/8"
response = requests.get(url)
data = response.json()
print(data)

# for item in data['data']:
#     print(item['name'])
    
