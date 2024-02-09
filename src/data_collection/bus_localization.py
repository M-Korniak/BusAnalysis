import requests
import time
import csv
import datetime

url = ('https://api.um.warszawa.pl/api/action/busestrams_get/'
       '?resource_id=%20f2e5503e-%20927d-4ad3-9500-4ab9e55deb59&'
       'apikey=2b03b1a7-89a1-478e-974e-c2049ab91a5c&type=1')


def get_bus_localization(how_many_minutes=60,
                         folder_path='/Users/michalkorniak/Documents/Programs'
                                     '/Python/PycharmProjects/BusAnalysis/data/'):
    current_time = time.strftime('%H:%M')
    localization_data = []
    for _ in range(3 * how_many_minutes):
        time.sleep(20)
        try:
            data = requests.get(url).json()
        except requests.exceptions.ConnectionError:
            continue
        if data['result'] != 'Błędna metoda lub parametry wywołania':
            loop_time = datetime.datetime.now()
            try:
                data['result'] = list(filter(lambda x: 60 > abs(datetime.datetime.
                                                                strptime(x['Time'], '%Y-%m-%d %H:%M:%S')
                                                                - loop_time).total_seconds(), data['result']))
            except ValueError:
                continue
            localization_data.extend(data['result'])

    with open(f'{folder_path}buses_localization_{current_time}.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Lines', 'VehicleNumber', 'Time', 'Lon', 'Lat'])
        localization_data.sort(key=lambda x: ((x['Lines']), int(x['VehicleNumber']),
                                              datetime.datetime.strptime(x['Time'], '%Y-%m-%d %H:%M:%S')))
        for bus in localization_data:
            csv_writer.writerow([bus['Lines'], bus['VehicleNumber'], bus['Time'],
                                 bus['Lon'], bus['Lat']])
