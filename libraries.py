import argparse
import requests
import json

# 1. Set up the parser
parser = argparse.ArgumentParser(description="Fetch flight data from the API.")
parser.add_argument("--date", type=str, required=True, help="Date in YYYY-MM-DD format")
parser.add_argument("--type", choices=["arrival", "departure"], default="arrival", help="Flight type")
parser.add_argument("--verbose", action="store_true", help="Print the full JSON response")

# 2. Parse the arguments
args = parser.parse_args()

# 3. Use them in your code
url = f"https://api.example.com/flights"
params = {"date": args.date, "type": args.type}  # Use args.date and args.type

response = requests.get(url, params=params)

if args.verbose:  # Only prints if user typed --verbose
    print(json.dumps(response.json(), indent=2))

# Continue with your existing loop logic...

import requests

# GET → Fetch data
resp = requests.get(url, params=)
# POST → Send/Create data
resp = requests.post(url)
# PUT → Replce/Update entirely
resp = requests.put(url)
# PATCH → Partial update
resp = requests.patch(url)
# DELETE → Remove
resp = requests.delete(url)
# HEAD → Headers only (no body)
resp = requests.head(url)
# OPTIONS → Allowed methods
resp = requests.options(url)
# Universal (dynamic method)
resp = requests.request(method="GET", url=url)

import logging
import logging

# Minimal setup: sets level and format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Now use the functions
logging.debug("This is for debugging (won't show at INFO level)")
logging.info("Script started successfully")
logging.warning("API response is slow")
logging.error("Failed to fetch data!")
logging.critical("System is down!")