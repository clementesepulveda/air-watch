import requests

res = requests.get('https://air-watch.onrender.com/')
response = res.status_code
print(response)