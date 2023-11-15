import pandas as pd
import json
from datetime import datetime
import yaml
import json

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

def optimize_files():
    # Convert YAML to JSON
    print('convert yaml to json')
    all_data = {
        "passengers": []
    }

    with open('downloads/passengers.yaml') as file:
        data = file.readlines()

        for i in range(int((len(data)-1)/8)):
            all_data["passengers"].append({
                "passengerID": data[i*8+1].strip().replace('"','').replace("- passengerID: ", ""),
                "firstName": data[i*8+2].strip().replace('"','').replace("firstName: ", ""),
                "lastName": data[i*8+3].strip().replace('"','').replace("lastName: ", ""),
                "birthDate": data[i*8+4].strip().replace('"','').replace("birthDate: ", ""),
                "gender": data[i*8+5].strip().replace('"','').replace("gender: ", ""),
                "height(cm)": data[i*8+6].strip().replace('"','').replace("height(cm): ", ""),
                "weight(kg)": data[i*8+7].strip().replace('"','').replace("weight(kg): ", ""),
                "avatar": data[i*8+8].strip().replace('"','').replace("avatar: ", ""),
            })

    print('saving as json')
    with open('downloads/passengers.json', 'w') as file:
        json.dump(all_data, file)

    ## ALL FLIGHTS TO ONE FILE
    print("merging flights")
    all_data = []
    for year in [i for i in range(2015, 2024)]:
        for month in [i for i in range(1, 13)]:
            file_name = f'downloads/flights/{year}/{month:02}/flight_data.json'
            with open(file_name) as file:
                data = json.loads(file.read())
                for flight in data:
                    flight['year'] = year
                    flight['month'] = month

                all_data += data

    with open("downloads/flights.json", "w") as file:
        json.dump(all_data, file)

    # read passengers
    print("giving passengers an age")
    with open(f'downloads/passengers.json') as f:
        passengers_json = json.loads(f.read())['passengers']
        passengers = pd.DataFrame.from_dict(passengers_json)
        passengers['passengerID']=passengers['passengerID'].astype(int)
        passengers['birthDate'] = passengers['birthDate'].apply(lambda x: spanish_to_english_date(x))

        passengers['age'] = ((datetime.now() - passengers['birthDate']).dt.days // 365.2425).astype(int)

    passengers.to_json('downloads/passengers.json')

    # read aircrafts
    aircrafts = pd.read_xml(f'downloads/aircrafts.xml')
    aircrafts = aircrafts.rename(columns={"name":"aircraftName"})
    aircrafts.to_json('downloads/aircrafts.json')

    # files to hdf
    files = [
        "aircrafts",
        'flights',
        'passengers',
    ]
    for file in files:
        df = pd.read_json(f'downloads/{file}.json')
        df.to_hdf(f'downloads/optimized_files/{file}.h5','df')

    df = pd.read_csv(f'downloads/airports.csv')
    df.to_hdf('downloads/optimized_files/airports.h5','df')
    df = pd.read_csv(f'downloads/tickets.csv')
    df.to_hdf('downloads/optimized_files/tickets.h5','df')

    # TICKETS PRECALC
    print('precalculating tickets')
    tickets = pd.read_csv('downloads//tickets.csv')
    passengers = pd.read_hdf('downloads/optimized_files/passengers.h5', 'df')
    tickets['passengerID']=tickets['passengerID'].astype(int)
    print(tickets.columns)
    print(passengers.columns)
    tickets = pd.merge(tickets,passengers, on="passengerID")
    tickets = tickets.groupby('flightNumber')['age'].agg(['sum','count'])
    tickets['averageAge'] = tickets['sum'] / tickets['count']
    tickets = tickets.rename(columns={"count":"passengersQty"})
    tickets = tickets.reset_index() 
    tickets.to_hdf('downloads/optimized_files/tickets.h5','df')


if __name__ == "__main__":
    print('starting')
    optimize_files()

    # aircrafts = pd.read_json('downloads/passengers.json')
    # aircrafts.to_hdf('downloads/optimized_files/passengers.h5', key='df', mode='w')
    # new_crafts = pd.read_hdf('downloads/optimized_files/passengers.h5', 'df')
    # print(new_crafts)