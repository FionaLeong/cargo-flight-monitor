import requests #python file for https request
from datetime import datetime
#from src.config import API_BASE_URL 


def fetch_flights(target_date=datetime.now().strftime('%Y-%m-%d'), cargo='true', arrival='false'):

    API_BASE= f"https://hongkongairport.com/flightinfo-rest/rest/flights"

    try:
        response = requests.get(API_BASE, params= {'span': '1', 'date': target_date, 'lang': 'en', 'cargo': cargo , 'arrival': arrival })
        response.raise_for_status()  # This will raise an error if status is not 200
    except requests.HTTPError as e:
        print(f"Error fetching arrival flights: {e}")
        return []  # Return an empty list on error

    data = response.json() #turn response into JSON object (key value pair) so that we can loop
    print(data[0])      #test print the jason 
    
    
    port_key = "origin" if arrival == "true" else "destination"

    #Flatten the nested JSON and save into list of record
    #can see the key of the dictionares through data[0].key
    flights = []
    for day_data in data: #each records
        for entry in day_data.get("list", []): #entry in each record
            for f in entry.get("flight", []):      #list in entry
                flights.append({
                    "flight_id": f"{f.get('no')}_{day_data.get('date')}",
                    "flight_no": f.get("no"),
                    "airline": f.get("airline"),
                    "date": day_data.get("date"),
                    "time": entry.get("time"),  
                    port_key: ",".join(entry.get(port_key, [])),       #dynamic based on the arrival or departure flag
                    "status": entry.get("status", ""),
                    "status_code": entry.get("statusCode"),
                    "flight_type": entry.get("flight_type"),   # since arrival is True for all
                    "last_updated": day_data.get("lastUpdatedTime", "")
            })
    return flights



#fix this so dynnamic, cargo and arrival flag

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

