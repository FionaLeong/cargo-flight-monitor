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