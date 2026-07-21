import os
from dotenv import load_dotenv

'''
essentially config.py is not needed as the API is public and no API key is needed. Hence, we can just directly use it in the api_client.py
but for scalablility (in case using paid cargo API), will include config.py
'''

load_dotenv() #looks for .env in the current directory, and brings the data in. this is because we can't import .env
#if load_env() is removed, will look for global system environment, and if haven't set, will return None

#reading variables/information from .env
#os.getenv("<VARIABLE_NAME>", <DEFAULT_VALUE> if key not found)
API_BASE_URL = os.getenv("API_BASE_URL") 
API_KEY = os.getenv("API_KEY")      #no API key
CURRENT_FILE = os.getenv("CURRENT_FILE", "data/current_flights.csv")
CHANGED_FILE = os.getenv("CHANGED_FILE", "data/changed_flights.csv")
NEWLY_CHANGED_FILE =os.getenv("NEWLY_CHANGED_FILE", "data/newly_changed_flights.csv")


