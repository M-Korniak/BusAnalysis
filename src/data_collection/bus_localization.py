import requests
import time
import csv
import datetime

url = ('https://api.um.warszawa.pl/api/action/busestrams_get/'
       '?resource_id=%20f2e5503e-%20927d-4ad3-9500-4ab9e55deb59&'
       'apikey=2b03b1a7-89a1-478e-974e-c2049ab91a5c&type=1&line=')


def get_bus_localization(bus_numbers, how_many_minutes=60,
                         folder_path='/Users/michalkorniak/Documents/Programs'
                                     '/Python/PycharmProjects/BusAnalysis/data/'):
    current_time = time.strftime('%H:%M')
    lines_data = {}
    for number in bus_numbers:
        lines_data[number] = []
    for _ in range(how_many_minutes):
        for number in bus_numbers:
            data = requests.get(url + number).json()
            if data['result'] != 'Błędna metoda lub parametry wywołania':
                lines_data[number].extend(data['result'])
        time.sleep(60)

    for number in bus_numbers:
        with open(f'{folder_path}bus_{number}_{current_time}.csv', 'w') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['VehicleNumber', 'Time', 'Lon', 'Lat'])
            lines_data[number].sort(key=lambda x: (int(x['VehicleNumber']),
                                                   datetime.datetime.strptime(x['Time'], '%Y-%m-%d %H:%M:%S')))
            for bus in lines_data[number]:
                csv_writer.writerow([bus['VehicleNumber'], bus['Time'],
                                     bus['Lon'], bus['Lat']])


if __name__ == '__main__':
    get_bus_localization(['167', '197'], 3)
