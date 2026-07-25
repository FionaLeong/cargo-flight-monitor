import logging
import argparse
from datetime import datetime, date
from src.api_client import fetch_arrival_flights, fetch_departure_flights
from src.data_processor import process_flights
from src.file_manager import write_current_snapshot

logging.basicConfig(level=logging.INFO) #basic logging from different libraries

def run(target_date):

    logging.info("Starting flight data extraction...")
    try:
        flights = fetch_departure_flights(target_date) #change to fetch_arrival_flights() for arrivals
        if not flights:     #raise a warning if no response from API
            logging.warning("No flights returned from API.")
            return

        full_df, changes = process_flights(flights)     #full df and newly status changes

      
        write_current_snapshot(full_df, target_date)         #write full snapshot of current flight status

        '''
        write_changed_snapshot(full_df, target_date)         #write filtered snapshot of changed flights
        append_changes(changes)               #write only newly changed flights
        '''
        
        logging.info(f"Saved {len(full_df)} flights; {len(changes)} new delayed/cancelled flights.")
    except Exception as e:
        logging.error(f"Run failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help='Date in YYYY-MM-DD format (defaults to today)')
    args = parser.parse_args()

    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        target_date = date.today()

    # Now call your run() function with the date
    run(target_date)