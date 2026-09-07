
cd /Users/fionaleong/HKIA_flight_monitor || exit 1

mkdir -p logs

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

LOG_FILE="logs/run_${TIMESTAMP}.log"

echo "========================================" >> "$LOG_FILE"    #save and create a file
echo "Run started at: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"          

#run the python scipt using .venv_HKIA
/Users/fionaleong/HKIA_flight_monitor/.venv_HKIA/bin/python -m src.main >> "$LOG_FILE" 2>&1

#scheduler won't run the script, fixed