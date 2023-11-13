## ALL FLIGHTS TO ONE FILE
# import json
# all_data = []
# for year in [i for i in range(2015, 2024)]:
#     for month in [i for i in range(1, 13)]:
#         file_name = f'flights/{year}/{month:02}/flight_data.json'
#         with open(file_name) as file:
#             data = json.loads(file.read())
#             for flight in data:
#                 flight['year'] = year
#                 flight['month'] = month

#             all_data += data

# # with open('flights.json', 'w') as file:
# #     file.write("["+',\n'.join(data) +"]")
# with open("flights.json", "w") as file:
#     json.dump(all_data, file)

## GIVE PASSENGERS AN AGE
import pandas as pd
import json
from datetime import datetime

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


    # read passengers
with open(f'passengers.json') as f:
    passengers_json = json.loads(f.read())['passengers']
    passengers = pd.DataFrame.from_dict(passengers_json)
    passengers['passengerID']=passengers['passengerID'].astype(int)
    passengers['birthDate'] = passengers['birthDate'].apply(lambda x: spanish_to_english_date(x))

    passengers['age'] = ((datetime.now() - passengers['birthDate']).dt.days // 365.2425).astype(int)

passengers.to_csv('passengers.csv', index=False)


test = pd.read_csv('passengers.csv')
print(test)
# if __name__ == "__main__":
#     import pandas as pd

#     data = pd.read_json('flights.json')
#     print(data)