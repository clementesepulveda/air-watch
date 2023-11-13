from google.cloud import storage
import os

def download_cs_file(bucket_name, file_name, destination_file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    dirname = os.path.dirname(destination_file_name)
    if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname)

    blob = bucket.blob(file_name)
    blob.download_to_filename(destination_file_name)

    return True

def download_files():
    # set key credentials file path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private_key.json'

    files = [
        'aircrafts.xml',
        'airports.csv',
        'passengers.yaml',
        'tickets.csv'
    ]

    for year in [i for i in range(2015, 2024)]:
        for month in [i for i in range(1, 13)]:
            files.append(f'flights/{year}/{month:02}/flight_data.json')

    for file in files:
        print('downloading', file)
        download_cs_file('2023-2-tarea3', file, f'./downloads/{file}')
        print('downloaded', file)
        print()

if __name__ == "__main__":
    download_files()
