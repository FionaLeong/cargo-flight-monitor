import pandas as pd
from src.file_manager import load_previous_snapshot

#this is for console outputting, outputting current flight from data frame and output newly changed data
def process_flights(current_flights):
    if not current_flights:
        print("Warning: No flights received from API. Skipping file update.")
        return pd.DataFrame(), []  # Return empty DataFrame, no changes
    
    full_df = pd.DataFrame(current_flights)
    previous_status = load_previous_snapshot() #return a dictionary {fid, status}

    changes = []
    for _, row in full_df.iterrows():
        fid = row["flight_id"]
        if row["status"] is None or pd.isna(row["status"]):
            current_status = ""
        else:
            current_status = row["status"].lower()
        prev = previous_status.get(fid)         #from each record in the current, search for the record in previous snapshoy
        
        if current_status in ("delayed", "cancelled"):
            if prev is None or str(prev).lower() not in ("delayed", "cancelled"): #will record newly change status
                changes.append(row.to_dict())       #change data frame (row records), to dictionary
    return full_df, changes 