import requests

headers = {'Authorization': 'Bearer 02303019856e83e300dfe6f71b7a1cfa68d31829'}

endpoint = "http://localhost:8000/api/products/"
# http://localhost:8000/admin/
# session -> post data
# selenium
get_response = requests.post(endpoint,json={"title":"Ring","price":"100"},headers=headers)
print(get_response.json())