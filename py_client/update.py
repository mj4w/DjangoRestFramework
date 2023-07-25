import requests

endpoint = "http://localhost:8000/api/products/1/update/"



get_response = requests.put(endpoint,json={"title":"Sunglasses","content":"New Brand","price":"20.00"})
print(get_response.json())