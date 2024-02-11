# BusAnalysis
## Introduction
This project is used to analyze the bus data of the city of Warsaw, Poland.
It allows to collect data, analyze it and visualize it using scripts written in Python.
## Data
The data is collected from the [ZTM API](https://api.um.warszawa.pl/) and is stored in the `data` directory.
## How to use
To use the scripts, you need to install the required packages using the following command:
```bash
pip install -r requirements.txt
```
You can run the script for collecting bus locations using the following command:
```bash
python scripts/collect_location.py --minutes 60 --folder data/
```
This will collect the bus locations every 60 minutes and store the data in the `data` directory.

To collect data about the bus stops, you can use the following command:
```bash
python scripts/collect_stops_info.py --folder data/
```

To analyze the data, you can use the following command:
```bash
python scripts/analyze_bus_data.py --path data/buses_location_HH:MM.csv --output_folder analysis/
```
This will analyze the data and store the results in the `analysis` directory.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References
- [ZTM API](https://api.um.warszawa.pl/)
- https://github.com/andilabs/warszawa-dzielnice-geojson/blob/master/warszawa.geojson

 

