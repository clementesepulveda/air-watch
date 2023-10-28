from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
import os
import pandas as pd
import yaml
from yaml import CLoader as Loader
import json
import glob
from datetime import datetime

app = FastAPI()

APP_FOLDER = "."

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def download_gcs_file(bucket_name, file_name, destination_file_name): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)

    dirname = os.path.dirname(destination_file_name)
    if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname)

    print(file_name)
    with open(destination_file_name, 'wb') as file_obj:
        blob.download_to_file(file_obj)
    # with open(destination_file_name, 'wb') as file_obj:
    #     blob.download_to_file(file_obj)
    # blob.download_to_filename(destination_file_name)

    return True

@app.get("/download_files")
async def download_files():
    for i in os.listdir():
        print(i)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f'{APP_FOLDER}/private_key.json'

    bucket_name = "2023-2-tarea3"

    files = [
        'aircrafts.xml',
        'airports.csv',
        'passengers.yaml',
        'tickets.csv'
    ]

    for year in [i for i in range(2015, 2024)]:
        for month in [i for i in range(1, 13)]:
            files.append(f'flights/{year}/{month:02}/flight_data.json')

    for file_name in files:
        download_gcs_file(bucket_name, file_name, f'{APP_FOLDER}/downloads/{file_name}')  
        if '.yaml' in file_name: # optimization for reading later
            with open(f'{APP_FOLDER}/downloads/{file_name}', 'r') as file:
                yaml_data = yaml.load(file, Loader=Loader)

            with open(f'{APP_FOLDER}/downloads/{file_name}'.replace('yaml', 'json'), 'w') as json_file:
                json.dump(yaml_data, json_file)

@app.get("/")
async def root():
    # await download_files()

    return {"message": "Hello World"}

def spanish_to_english_date(d):
    mapping_dict = {
        'enero':'january',
        'febrero':'february',
        'marzo':'march',
        'abril':'april',
        'mayo':'may',
        'junio':'june',
        'julio':'july',
        'agosto':'august',
        'septiembre':'september',
        'octubre':'october',
        'noviembre':'november',
        'diciembre':'dicember'
    }
    
    d = d.replace(d.split(" ")[2], mapping_dict[d.split(" ")[2]])
    d = d.replace("de ", "")
    datetime_object = datetime.strptime(d, '%d %B %Y')
    return datetime_object

@app.get("/vuelos")
def vuelos():
    # read flights
    root_directory = f'{APP_FOLDER}/downloads/flights/'
    json_pattern = os.path.join(root_directory, '**', '*.json')
    file_list = glob.glob(json_pattern, recursive=True)
    
    temp = []
    for file in file_list:
        data = pd.read_json(file)
        temp.append(data)
    
    flights = pd.concat(temp, ignore_index=True)

    # # read aircrafts
    # # TODO, doesnt have root node
    aircrafts = pd.read_xml(f'{APP_FOLDER}/downloads/aircrafts.xml')
    aircrafts = aircrafts.rename(columns={"name":"aircraftName"})
    flights = pd.concat([flights, aircrafts], axis=1, join="inner")

    # # read airports
    # # TODO, some lines have , in them. 
    airports = pd.read_csv(f'{APP_FOLDER}/downloads/airports.csv', on_bad_lines='skip')
    flights = pd.merge(flights, airports, left_on="originIATA", right_on="airportIATA")
    flights = flights.rename(columns={"country":"origin"})
    flights = pd.merge(flights, airports, left_on="destinationIATA", right_on="airportIATA")
    flights = flights.rename(columns={"country":"destination"})

    # read tickets  
    with open(f'{APP_FOLDER}/downloads/tickets.csv') as f:
        tickets = pd.read_csv(f)
        tickets['passengerID']=tickets['passengerID'].astype(int)

    # read passengers
    with open(f'{APP_FOLDER}/downloads/passengers.json') as f:
        passengers_json = json.loads(f.read())['passengers']
        passengers = pd.DataFrame.from_dict(passengers_json)
        passengers['passengerID']=passengers['passengerID'].astype(int)
        passengers['birthDate'] = passengers['birthDate'].apply(lambda x: spanish_to_english_date(x))

        passengers['age'] = (datetime.now() - passengers['birthDate']).dt.days // 365.2425

    passengers = pd.merge(tickets,passengers, on="passengerID")
    passengers = passengers.groupby('flightNumber')['age'].agg(['sum','count'])
    passengers['averageAge'] = passengers['sum'] / passengers['count']
    passengers = passengers.rename(columns={"count":"passengersQty"})
    passengers = passengers.reset_index()
    
    flights = pd.merge(flights, passengers, on="flightNumber")
    # print(tickets)
    # for col in passengers.columns:
    #     print(col)
    # print(passengers) 

    return flights.to_dict('records')
    return ""

@app.get("/vuelo/{flight_id}")
def vuelo(flight_id: str):
    return {
        ""
    }