# Dynamic Pricing for flight information
---
The below source code does an extraction of cargo flight information to determine whether there are any changes such in flight status, especially 'cancelled' and 'delayed'. Upon determining changes in flight status, cargo prices can be adjust accordingly for dynamic pricing purposes


## folder cofiguration
```tree
cargo_flight_monitor
├── __init__.py
├── data
│   ├── changed_flights.csv
│   └── current_flights.csv
├── README.md
├── requirements.txt
└── src
    ├── __init__.py
    ├── api_client.py
    ├── config.py
    ├── data_processor.py
    ├── file_manager.py
    └── main.py
```

## 1. data
data are selected on a daily basis

- **changed_flights.csv** track flight changes by detecting flight status that are cancelled or delayed

- **current_flights.csv** track daily flights information
## 2. src

- **config.py**

    -load .env and get .env as a global variable to be used in src file

- **api_client.py**

    -send a get request to extract flight information, flatten in JSON format, then loop through to store the data
    
    -two functions: **fetch_arrival_flights** and **fetch_departure_flights**

- **
