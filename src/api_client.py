import requests #python file for https request
from datetime import datetime
#from src.config import API_BASE_URL 

def fetch_arrival_flights(target_date):
    """
    Fetch flights from Hong Kong Airport API.
    """

    API_BASE= f"https://hongkongairport.com/flightinfo-rest/rest/flights?span=1&date={target_date}&lang=en&cargo=true&arrival=true"


    try:
        response = requests.get(API_BASE)
        response.raise_for_status()  # This will raise an error if status is not 200
    except requests.HTTPError as e:
        print(f"Error fetching arrival flights: {e}")
        return []  # Return an empty list on error

    data = response.json() #turn response into JSON object (key value pair) so that we can loop
    
    # Flatten the nested JSON and save into list of record
    # can see the key of the dictionares through data[0].key
    flights_arrival = []
    for day_data in data:
        for entry in day_data.get("list", []):
            for f in entry.get("flight", []):
                flights_arrival.append({
                    "flight_id": f"{f.get('no')}_{day_data.get('date')}",
                    "flight_no": f.get("no"),
                    "airline": f.get("airline"),
                    "date": day_data.get("date"),
                    "time": entry.get("time"),
                    "origin": ", ".join(entry.get("origin", [])),
                    "status": entry.get("status", ""),
                    "status_code": entry.get("statusCode"),
                    "flight_type": "arrival",   # since arrival is True for all
                    "last_updated": day_data.get("lastUpdatedTime", "")
            })
    return flights_arrival


def fetch_departure_flights(target_date):
    

    API_BASE= f"https://hongkongairport.com/flightinfo-rest/rest/flights?span=1&date={target_date}&lang=en&cargo=true&arrival=false"

    try:
        response = requests.get(API_BASE)
        response.raise_for_status() # This will raise an error if status is not 200
        print(response.status_code)
    except requests.HTTPError as e:
        print(f'Error fetching departure flights: {e}')
        return []  # Return an empty list on error
    
    data = response.json()
    
    #Flatten the nested JSON into a list of flight records
    flights_departure = []
    for day_data in data:       #each record
        for entry in day_data.get("list", []):          #each entry in one record
            for f in entry.get("flight", []):                   #list entry
                flights_departure.append({
                    "flight_id": f"{f.get('no')}_{day_data.get('date')}",
                    "flight_no": f.get("no"),
                    "airline": f.get("airline"),
                    "date": day_data.get("date"),
                    "time": entry.get("time"),
                    "destination": ", ".join(entry.get("destination", [])),
                    "status": entry.get("status", ""),
                    "status_code": entry.get("statusCode"),
                    "flight_type": "departure", 
                    "last_updated": day_data.get("lastUpdatedTime", "")
            })

    return flights_departure

#JSON file format for parsing both arrival and departure
'''
{"date":"2026-07-07",
"arrival":false,
"cargo":true,
"list":[{"time":"14:40","flight":[{"no":"WW 862D","airline":"KXP"}],
"status":"Dep 06:41 (15/07/2026)",
"statusCode":null,
"destination":["KUL"]}],
"lastUpdatedTime":"2026-07-15T09:59:02+08:00"}
'''

