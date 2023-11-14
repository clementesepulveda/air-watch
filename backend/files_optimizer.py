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
            if i % 1000 == 0:
                print(i)

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
                print("  reading", file_name)
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

    passengers.to_csv('downloads/passengers.csv', index=False)

if __name__ == "__main__":
    print('starting')
    optimize_files()
    