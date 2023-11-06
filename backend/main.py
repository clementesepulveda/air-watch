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

from fastapi_utils.tasks import repeat_every
import asyncio
from celery import Celery
import requests

# app2 = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')



app = FastAPI()


APP_FOLDER = "."

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
@repeat_every(seconds=60 * 10)  # 10 minutes
def call_front():
    res = requests.get('https://air-watch.onrender.com/')
    response = json.loads(res.text)
    print(response)

# @app2.task
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
        if '.yaml' in file_name: # optimization for reading later
            with open(f'{APP_FOLDER}/downloads/{file_name}', 'r') as file:
                yaml_data = yaml.load(file, Loader=Loader)

            with open(f'{APP_FOLDER}/downloads/{file_name}'.replace('yaml', 'json'), 'w') as json_file:
                json.dump(yaml_data, json_file)
            

    return True

# @app.on_event("startup")
# @repeat_every(seconds=10)  # 1 hour
@app.get("/download_files")
def download_files(): # background_task: BackgroundTasks
    print("Starting download.")

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
        # background_task.add_task(download_gcs_file, bucket_name, file_name, f'{APP_FOLDER}/downloads/{file_name}')
        download_gcs_file(bucket_name, file_name, f'{APP_FOLDER}/downloads/{file_name}')  

    return {"message": "Files are currently downloading."}

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
        'diciembre':'december'
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
        print('reading', file)
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

    return flights.to_dict('records')

@app.get("/vuelo/{flight_number}")
def vuelo(flight_number: int):
    
    # # read flights
    root_directory = f'{APP_FOLDER}/downloads/flights/'
    json_pattern = os.path.join(root_directory, '**', '*.json')
    file_list = glob.glob(json_pattern, recursive=True)
    
    temp = []
    for file in file_list:
        data = pd.read_json(file)
        temp.append(data)
    
    flights = pd.concat(temp, ignore_index=True)
    flight = flights[ flights["flightNumber"]==flight_number ]

    # read aircrafts
    # TODO, doesnt have root node
    aircrafts = pd.read_xml(f'{APP_FOLDER}/downloads/aircrafts.xml')
    aircraft = pd.concat([flight, aircrafts], axis=1, join="inner")
    aircraft = aircraft[ ['name','aircraftType']]

    # read airports
    # TODO, some lines have , in them. 
    airports = pd.read_csv(f'{APP_FOLDER}/downloads/airports.csv', on_bad_lines='skip')
    airports = [
        pd.merge(flight, airports, left_on="originIATA", right_on="airportIATA"),
        pd.merge(flight, airports, left_on="destinationIATA", right_on="airportIATA")
    ]
    airports[0] = airports[0][ ['name','city','country','lat','lon']].to_dict('records')[0]
    airports[1] = airports[1][ ['name','city','country','lat','lon']].to_dict('records')[0]

    # read tickets  
    with open(f'{APP_FOLDER}/downloads/tickets.csv') as f:
        tickets = pd.read_csv(f)
        tickets['passengerID']=tickets['passengerID'].astype(int)
        tickets = tickets[ tickets['flightNumber'] == flight_number]

    # read passengers
    with open(f'{APP_FOLDER}/downloads/passengers.json') as f:
        passengers_json = json.loads(f.read())['passengers']
        passengers = pd.DataFrame.from_dict(passengers_json)
        passengers['passengerID']=passengers['passengerID'].astype(int)
        passengers['birthDate'] = passengers['birthDate'].apply(lambda x: spanish_to_english_date(x))

        passengers['age'] = (datetime.now() - passengers['birthDate']).dt.days // 365.2425

    passengers = pd.merge(tickets, passengers, on="passengerID")
    passengers = passengers[['passengerID','avatar','firstName','lastName','seatNumber','age','gender','weight(kg)','height(cm)']]

    aircraft = aircraft.to_dict('records')
    passengers = passengers.to_dict('records')
    flight = flight[ ['flightNumber', 'airline'] ].to_dict('records')[0]

    return {
        'flight': flight,
        'airports': airports,
        'aircraft': aircraft[0] if aircraft else {},
        'passengers': passengers,
    }
