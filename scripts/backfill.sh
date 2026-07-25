#!/bin/bash

# =============================================================
# BACKFILL SCRIPT - Runs src.main for every date in a range
# =============================================================


# Navigate to your project root
cd /Users/fionaleong/cargo_flight_monitor || exit 1

# Create logs folder if it doesn't exist
mkdir -p back_logs

# ================= CONFIGURE YOUR DATE RANGE =================
START_DATE=$(date -v-91d +%Y-%m-%d) # Change this to your earliest desired date
END_DATE=$(date -v+2d +%Y-%m-%d) 
# =============================================================
# Convert dates to epoch seconds (macOS compatible)
start_epoch=$(date -j -f "%Y-%m-%d" "$START_DATE" +%s)
end_epoch=$(date -j -f "%Y-%m-%d" "$END_DATE" +%s)

current_epoch=$start_epoch

echo "========================================" | tee -a "back_logs/backfill.log"
echo "$(date): Starting backfill from $START_DATE to $END_DATE" | tee -a "back_logs/backfill.log"
echo "========================================" | tee -a "back_logs/backfill.log"

# Python interpreter path
PYTHON_CMD="/Users/fionaleong/cargo_flight_monitor/.venv/bin/python"


while [[ $current_epoch -le $end_epoch ]]; do

    
    # Convert epoch back to YYYY-MM-DD
    current_date=$(date -j -f "%s" "$current_epoch" +%Y-%m-%d)
    BACKLOG_FILE="back_logs/run_${current_date}.backlog"
    
    echo "$(date): Running src.main for ${current_date}..." | tee -a "back_logs/backfill.log"
    
    # =============================================================
    # EXECUTE YOUR PYTHON SCRIPT WITH THE DATE
    # =============================================================
    $PYTHON_CMD -m src.main --date "$current_date" >> "$BACKLOG_FILE" 2>&1
    
    # Capture the exit code (0 = success, anything else = failure)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "$(date): Successfully processed ${current_date}" | tee -a "back_logs/backfill.log"
    else
        echo "$(date): Failed to process ${current_date} (Exit code: ${exit_code})" | tee -a "back_logs/backfill.log"
    fi
    
    # Wait 1 second to be gentle on the API / database
    sleep 1
    
    # Move to the next day (86400 seconds = 24 hours)
    current_epoch=$((current_epoch + 86400))
done

echo "========================================" | tee -a "back_logs/backfill.log"
echo "$(date): 🎉 Backfill completed!" | tee -a "back_logs/backfill.log"
echo "========================================" | tee -a "back_logs/backfill.log"