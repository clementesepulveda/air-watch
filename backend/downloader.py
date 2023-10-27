# import packages
from google.cloud import storage
import os

# set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private_key.json'

# Bucket-name: “2023-2-tarea3"
# ProjectID: “taller-integracion-310700"

# define function that downloads a file from the bucket
def download_cs_file(bucket_name, file_name, destination_file_name): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True

files = [
    'flights/2015/01/flight_data.json',
    'aircrafts.xml'
]

for file in files:
    download_cs_file('2023-2-tarea3', file, f'./downloads/{file}')
