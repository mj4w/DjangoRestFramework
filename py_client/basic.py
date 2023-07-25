import requests

# endpoint = "https://httpbin.org/status/200/"
# endpoint = "https://httpbin.org/anything"
endpoint = "http://localhost:8000/api/"

get_response = requests.post(endpoint,json={"title":"Title Sample","content":"Hello World","price":"123"}) # HTTP REQUEST Application programming interface


# print(get_response.headers)
# print(get_response.text)

# REST APIs -> Web Based Api

# print(get_response.text)

# HTTP Request -> HTML
# REST API HTTP Request -> JSON

print(get_response.json())