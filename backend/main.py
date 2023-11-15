from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd

import time

from downloader import download_files
from files_optimizer import optimize_files

app = FastAPI()


APP_FOLDER = "."

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/download_files")
def download_files_endpoint(background_tasks: BackgroundTasks):
    download_files()
    optimize_files()
    return {"message": "Files downloaded."}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./favicon.ico")

@app.get("/vuelos")
def vuelos():
    TIMES_TO_RUN = 1
    total_time = time.time()
    debug_timer = time.time()
    # read flights
    for _ in range(TIMES_TO_RUN):
        flights = pd.read_hdf('downloads/optimized_files/flights.h5', 'df')

    # print('read flights', time.time()- debug_timer)
    debug_timer = time.time()
    # # read aircrafts
    STARTING_FLIGHTS = flights.copy()
    for _ in range(TIMES_TO_RUN):
        aircrafts = pd.read_hdf(f'downloads/optimized_files/aircrafts.h5','df')
        flights = pd.concat([flights, aircrafts], axis=1, join="inner")
    
    # print('read aircrafts', time.time()- debug_timer)
    debug_timer = time.time()
    for _ in range(TIMES_TO_RUN):
        airports = pd.read_hdf(f'downloads/optimized_files/airports.h5', 'df')
        flights = STARTING_FLIGHTS.copy()
        flights = pd.merge(flights, airports, left_on="originIATA", right_on="airportIATA")
        flights = flights.rename(columns={"country":"origin"})
        flights = pd.merge(flights, airports, left_on="destinationIATA", right_on="airportIATA")
        flights = flights.rename(columns={"country":"destination"})

    # print('merge airports', time.time()- debug_timer)
    debug_timer = time.time()
    # read tickets  
    for _ in range(TIMES_TO_RUN):
        tickets = pd.read_hdf('downloads/optimized_files/tickets.h5','df')

    # print('read tickets', time.time()- debug_timer)
    debug_timer = time.time()
    # read passengers
    for _ in range(TIMES_TO_RUN):
        passengers = pd.read_hdf('downloads/optimized_files/passengers.h5', 'df')
        # passengers = pd.read_json(f'{APP_FOLDER}/downloads/passengers.json')

    # print('read passengers.h5', time.time()- debug_timer)

    # debug_timer = time.time()
    # STARTING_PASS = tickets.copy()
    # for _ in range(TIMES_TO_RUN):
    #     tickets = STARTING_PASS.copy()
    #     tickets = pd.merge(tickets,passengers, on="passengerID")
    #     tickets = tickets.groupby('flightNumber')['age'].agg(['sum','count'])
    #     tickets['averageAge'] = tickets['sum'] / tickets['count']
    #     tickets = tickets.rename(columns={"count":"passengersQty"})
    #     tickets = tickets.reset_index()
        
    flights = pd.merge(flights, tickets, on="flightNumber")
    # print('merge tickets', time.time()- debug_timer)

    debug_timer = time.time()
    # total distance
    for _ in range(TIMES_TO_RUN):
        flights['distance'] = ((flights['lat_x'] - flights['lat_y'])**2 + (flights['lon_x']-flights['lon_y'])**2)**(1/2)

    # print('read distante', time.time()- debug_timer)

    STARTING_FLIGHTS = flights.copy()
    debug_timer = time.time()
    for _ in range(TIMES_TO_RUN):
        flights = STARTING_FLIGHTS.copy()
        flights = flights.to_dict('records')
    # print('flights to dict', time.time()- debug_timer)

    print('TOTAL TIME', time.time() - total_time)
    return flights
    

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

@app.get("/temporal_data")
def temporal_data(year: int = None, characteristics: str = ""):
    if characteristics not in ['distance', 'weight', 'height']:
        return {'error': 'characteristics needs to be distance, weight or height'}
    
    # read flights
    flights = pd.read_json('downloads/flights.json')
    if year != None:
        flights = flights[flights['year'] == year]

    months = [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ]

    if characteristics == "distance":
        # read airports
        airports = pd.read_csv(f'{APP_FOLDER}/downloads/airports.csv', on_bad_lines='skip')
        flights = pd.merge(flights, airports, left_on="originIATA", right_on="airportIATA")
        flights = flights.rename(columns={"country":"origin"})
        flights = pd.merge(flights, airports, left_on="destinationIATA", right_on="airportIATA")
        flights = flights.rename(columns={"country":"destination"})

        # total distance
        flights['distance'] = ((flights['lat_x'] - flights['lat_y'])**2 + (flights['lon_x']-flights['lon_y'])**2)**(1/2)
        flights = flights[['distance', 'month']].groupby('month').sum().reset_index().rename(columns={"distance": "value"})
        
        flights['month'] = flights['month'].apply(lambda x: months[x-1])

        return flights.to_dict('records')
    else:
        with open(f'{APP_FOLDER}/downloads/tickets.csv') as f:
            tickets = pd.read_csv(f)
            tickets['passengerID']=tickets['passengerID'].astype(int)

        # read passengers
        passengers = pd.read_csv(f'{APP_FOLDER}/downloads/passengers.csv')

        passengers = pd.merge(tickets,passengers, on="passengerID")
        flights = pd.merge(flights, passengers, on="flightNumber")

        if characteristics == "weight":
            flights = flights[['month', 'weight(kg)']].groupby('month').mean().reset_index().rename(columns={"weight(kg)": "value"})
            flights['month'] = flights['month'].apply(lambda x: months[x-1])
            return flights.to_dict('records')
        elif characteristics == "height":
            flights = flights[['month', 'height(cm)']].groupby('month').mean().reset_index().rename(columns={"height(cm)": "value"})
            flights['month'] = flights['month'].apply(lambda x: months[x-1])
            return flights.to_dict('records')

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
    passengers = passengers[passengers['passengerID'].isin(tickets['passengerID'])]

    all_age_values = pd.DataFrame({'age': range(1, 100)})

    males = passengers[passengers['gender'] == 'male'].groupby('age').count().reset_index()[['age','passengerID']]
    males = males.rename(columns={'passengerID': 'qty'})
    males = pd.merge(all_age_values, males, on='age', how='left')
    males['qty'].fillna(0, inplace=True)
    males = males.set_index('age')['qty'].to_dict()

    females = passengers[passengers['gender'] == 'female'].groupby('age').count().reset_index()[['age','passengerID']]
    females = females.rename(columns={'passengerID': 'qty'})
    females = pd.merge(all_age_values, females, on='age', how='left')
    females['qty'].fillna(0, inplace=True)
    females = females.set_index('age')['qty'].to_dict()
    
    ret_data = {
        'males': males,
        'females': females,
    }
    return ret_data
