import requests

res = requests.get('https://air-watch-api.onrender.com/')
response = res.status_code
print(response)