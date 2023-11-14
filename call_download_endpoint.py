import requests

res = requests.get('https://tarea-3-iic3103-backend.onrender.com/download_files')
response = res.status_code
print(response)