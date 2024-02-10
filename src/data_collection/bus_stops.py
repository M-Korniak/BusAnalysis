import requests
import csv


def timetable_at_stop(stop_lines, folder_path='/Users/michalkorniak/Documents/Programs'
                                              '/Python/PycharmProjects/BusAnalysis/data/'):
    apikey = '2b03b1a7-89a1-478e-974e-c2049ab91a5c'
    url = 'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238'

    with open(f'{folder_path}timetable.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Stop_Id', 'Stop_Nr', 'Lines', 'Timetable'])
        for stop in stop_lines:
            stop_id = stop.get('stop_id', '')
            stop_nr = stop.get('stop_nr', '')
            line = stop.get('line', '')
            print(stop_id)
            if stop_id and stop_nr and line:
                try:
                    data = requests.get(f'{url}&busstopId={stop_id}'
                                        f'&busstopNr={stop_nr}&line={line}&apikey={apikey}').json()
                except requests.exceptions.ConnectionError:
                    continue
                for stop_data in data['result']:
                    for timetable in stop_data['values']:
                        if timetable['key'] == 'czas':
                            csv_writer.writerow([stop_id, stop_nr, line, timetable['value']])


def lines_at_stop(stops, folder_path='/Users/michalkorniak/Documents/Programs/'
                                     'Python/PycharmProjects/BusAnalysis/data/'):
    apikey = '2b03b1a7-89a1-478e-974e-c2049ab91a5c'
    url = ('https://api.um.warszawa.pl/api/action/dbtimetable_get/'
           '?id=88cd555f-6f31-43ca-9de4-66c479ad5942')
    lines = []
    for stop in stops:
        stop_id = stop.get('zespol', '')
        stop_nr = stop.get('slupek', '')
        if stop_id and stop_nr:
            try:
                data = requests.get(f'{url}&busstopId={stop_id}&busstopNr={stop_nr}&apikey={apikey}').json()
            except requests.exceptions.ConnectionError:
                continue
            for line in data['result']:
                if len(line['values'][0]['value']) == 3:
                    print(stop_id, stop_nr, line['values'][0]['value'])
                    lines.append({'stop_id': stop_id, 'stop_nr': stop_nr, 'line': line['values'][0]['value']})

    timetable_at_stop(lines, folder_path)

    with open(f'{folder_path}bus_lines_at_stops.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Stop_Id', 'Stop_Nr', 'Lines'])
        for line in lines:
            csv_writer.writerow([line['stop_id'], line['stop_nr'], line['line']])


def get_bus_stops(folder_path='/Users/michalkorniak/Documents/Programs'
                              '/Python/PycharmProjects/BusAnalysis/data/'):
    url = ('https://api.um.warszawa.pl/api/action/dbstore_get/'
           '?id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&sortBy=id'
           '&apikey=2b03b1a7-89a1-478e-974e-c2049ab91a5c')

    valuable_keys = ['zespol', 'slupek', 'dlug_geo', 'szer_geo']

    data = requests.get(url).json()['result']
    output = []
    for stop in data:
        stop_data = {}
        for information in stop['values']:
            if information['key'] in valuable_keys:
                stop_data[information['key']] = information['value']
        output.append(stop_data)

    lines_at_stop(output, folder_path)

    with open(f'{folder_path}bus_stops.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Stop_Id', 'Stop_Nr', 'Lon', 'Lat'])
        for stop in output:
            csv_writer.writerow([stop.get('zespol', ''), stop.get('slupek', ''),
                                 stop.get('dlug_geo', ''), stop.get('szer_geo', '')])
