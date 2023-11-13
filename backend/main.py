from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from google.cloud import storage
import os
import pandas as pd
import yaml
from yaml import CLoader as Loader
import json
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

    if '.yaml' in file_name: 
        # Convert YAML to JSON
        with open(f'{APP_FOLDER}/downloads/{file_name}', 'r') as file:
            yaml_data = yaml.load(file, Loader=Loader)

        with open(f'{APP_FOLDER}/downloads/{file_name}'.replace('yaml', 'json'), 'w') as json_file:
            json.dump(yaml_data, json_file)
            
    return True

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

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./favicon.ico")


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
    flights = pd.read_json('downloads/flights.json')

    # # read aircrafts
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
    passengers = pd.read_csv(f'{APP_FOLDER}/downloads/passengers.csv')

    passengers = pd.merge(tickets,passengers, on="passengerID")
    passengers = passengers.groupby('flightNumber')['age'].agg(['sum','count'])
    passengers['averageAge'] = passengers['sum'] / passengers['count']
    passengers = passengers.rename(columns={"count":"passengersQty"})
    passengers = passengers.reset_index()
    
    flights = pd.merge(flights, passengers, on="flightNumber")

    # total distance
    flights['distance'] = ((flights['lat_x'] - flights['lat_y'])**2 + (flights['lon_x']-flights['lon_y'])**2)**(1/2)

    return flights.to_dict('records')

@app.get("/vuelo/{flight_number}")
def vuelo(flight_number: int):
    # read flights
    flights = pd.read_json('downloads/flights.json')
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
    passengers = pd.read_csv(f'{APP_FOLDER}/downloads/passengers.csv')

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

@app.get("/vuelos_cantidad_data/")
def data_cantidad(year: int = None, flight_class: str = None):
    # read flights
    flights = pd.read_json('downloads/flights.json')
    if year != None:
        flights = flights[flights['year'] == year]

    # read tickets  
    with open(f'{APP_FOLDER}/downloads/tickets.csv') as f:
        tickets = pd.read_csv(f)
        if flight_class != None:
            tickets = tickets[tickets['flightType'] == flight_class]
            
    tickets = tickets[tickets['flightNumber'].isin(flights['flightNumber'])]
    
    tickets = tickets.groupby(by="flightNumber").count()['ticketID'].reset_index().rename(columns={"ticketID": "total_passengers"})
    flights = pd.merge(flights, tickets, how='inner', on="flightNumber")[['airline','total_passengers']]
    flights = flights.groupby(by="airline").sum().reset_index()
    return flights.to_dict('records')

@app.get("/population_data")
def data_poblacion(year: int = None):
    # read flights
    flights = pd.read_json('downloads/flights.json')
    if year != None:
        flights = flights[flights['year'] == year]

    # read tickets  
    with open(f'{APP_FOLDER}/downloads/tickets.csv') as f:
        tickets = pd.read_csv(f)
            
    tickets = tickets[tickets['flightNumber'].isin(flights['flightNumber'])]

    # read passengers
    passengers = pd.read_csv(f'{APP_FOLDER}/downloads/passengers.csv')
    
    all_age_values = pd.DataFrame({'age': range(1, 100)})


    males = passengers[passengers['gender'] == 'male'].groupby('age').count().reset_index()[['age','passengerID']]
    males = males.rename(columns={'passengerID': 'qty'})
    males = pd.merge(all_age_values, males, on='age', how='left')
    males['qty'].fillna(0, inplace=True)
    males = males.set_index('age')['qty'].to_dict()
    print()

    females = passengers[passengers['gender'] == 'female'].groupby('age').count().reset_index()[['age','passengerID']]
    females = females.rename(columns={'passengerID': 'qty'})
    females = pd.merge(all_age_values, females, on='age', how='left')
    females['qty'].fillna(0, inplace=True)
    females = females.set_index('age')['qty'].to_dict()
    
    ret_data = {
        'males': males,
        'females': females,
    }
    print(ret_data)
    return ret_data