#!/bin/bash

# Navigate to your project root
cd /Users/fionaleong/cargo_flight_monitor || exit 1

# Create logs folder if it doesn't exist
mkdir -p back_logs

# ================= CONFIGURE YOUR DATE RANGE =================

'''
#hardcode date
START_DATE='2028-08-18'
END_DATE='2028-08-20'
'''
#date range for backfill
START_DATE=$(date -v-91d +%Y-%m-%d) #change this to your earliest desired date
END_DATE=$(date -v+2d %Y-%m-%d) 

# =============================================================
# Convert dates to epoch seconds (macOS compatible)
start_epoch=$(date -j -f "%Y-%m-%d" "$START_DATE" +%s)
end_epoch=$(date -j -f "%Y-%m-%d" "$END_DATE" +%s)

current_epoch=$start_epoch

echo "========================================" | tee -a "back_logs/backfill.log"
echo "$(date): Starting backfill from $START_DATE to $END_DATE" | tee -a "back_logs/backfill.log"
echo "========================================" | tee -a "back_logs/backfill.log"

# Python interpreter path
PYTHON_CMD="/Users/fionaleong/cargo_flight_monitor/.venv_HKIA/bin/python"

# cargo arrival flag

CARGO_FLAG = "true"
ARRIVAL_FLAG= "false"


while [[ $current_epoch -le $end_epoch ]]; do

    
    # Convert epoch back to YYYY-MM-DD
    current_date=$(date -j -f "%s" "$current_epoch" +%Y-%m-%d)
    BACKLOG_FILE="back_logs/run_${current_date}.backlog"
    
    echo "$(date): Running src.main for ${current_date}..." | tee -a "back_logs/backfill.log"
    

    $PYTHON_CMD -m src.main --date "$current_date" --cargo "$CARGO_FLAG" --arrival "$ARRIVAL_FLAG" >> "$BACKLOG_FILE" 2>&1
    
    # Capture the exit code (0 = success, anything else = failure)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "$(date): Successfully processed ${current_date}" | tee -a "back_logs/backfill.log"
    else
        echo "$(date): Failed to process ${current_date} (Exit code: ${exit_code})" | tee -a "back_logs/backfill.log"
    fi
    
    #wait 1 second before next iteration 
    sleep 1
    
    # Move to the next day (86400 seconds = 24 hours)
    current_epoch=$((current_epoch + 86400))
done

echo "========================================" | tee -a "back_logs/backfill.log"
echo "$(date): Backfill completed!" | tee -a "back_logs/backfill.log"
echo "========================================" | tee -a "back_logs/backfill.log"