
cd /Users/fionaleong/cargo_flight_monitor || exit 1

mkdir -p logs

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

LOG_FILE="logs/run_${TIMESTAMP}.log"

echo "========================================" >> "$LOG_FILE"    #save and create a file
echo "Run started at: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"          

/Users/fionaleong/cargo_flight_monitor/.venv/bin/python -m src.main >> "$LOG_FILE" 2>&1
