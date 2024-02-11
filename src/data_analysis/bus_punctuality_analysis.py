import pandas as pd
import datetime
import numpy as np


def calculate_distance(lon1, lat1, lon2, lat2):
    # https://en.wikipedia.org/wiki/Haversine_formula
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    lon_len = lon2 - lon1
    lat_len = lat2 - lat1
    a = np.sin(lat_len / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon_len / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return 6371 * c


def calculate_time_difference(time1, time2):
    if len(time1) > 8:
        time1 = time1[-8:]
    if len(time2) > 8:
        time2 = time2[-8:]

    time1 = datetime.datetime.strptime(time1, '%H:%M:%S')
    time2 = datetime.datetime.strptime(time2, '%H:%M:%S')

    return abs((time2 - time1).total_seconds())


def add_delay_column(data, timetable):
    delay = []

    for i in range(len(timetable)):
        stop = timetable.iloc[i]
        bus = data[(data['Lines'] == stop['Lines']) &
                   (calculate_distance(data['Lon'], data['Lat'], stop['Lon'], stop['Lat']) < 0.3)]

        if len(bus) == 0:
            delay.append(np.nan)
            continue

        min_time_difference = calculate_time_difference(bus.iloc[0]['Time'], stop['Time'])
        for j in range(len(bus)):
            if calculate_time_difference(bus.iloc[j]['Time'], stop['Time']) < min_time_difference:
                min_time_difference = calculate_time_difference(bus.iloc[j]['Time'], stop['Time'])
        delay.append(min_time_difference)

    timetable['Delay'] = delay

    return timetable


def bus_stops_punctuality(path_to_bus_localization='data/buses_localization_16:00.csv',
                          path_to_bus_stops='data/stops.csv',
                          path_to_timetable='data/timetable.csv'):
    data = pd.read_csv(path_to_bus_localization,
                       dtype={'Lines': str, 'VehicleNumber': str, 'Time': str, 'Lon': float, 'Lat': float})
    stops = pd.read_csv(path_to_bus_stops,
                        dtype={'Stop_Id': str, 'Stop_Nr': str, 'Lon': float, 'Lat': float})
    timetable = pd.read_csv(path_to_timetable,
                            dtype={'Stop_Id': str, 'Stop_Nr': str, 'Lines': str, 'Time': str})

    data = data.sort_values(by='Time')
    data = data.iloc[int(len(data) * 0.1):int(len(data) * 0.9)]
    data = data.reset_index(drop=True)

    min_time = data['Time'].min()[11:19]
    max_time = data['Time'].max()[11:19]

    timetable = timetable[timetable['Time'] >= min_time]
    timetable = timetable[timetable['Time'] <= max_time]
    timetable.reset_index(drop=True, inplace=True)
    timetable = timetable.merge(stops, on=['Stop_Id', 'Stop_Nr'])

    return add_delay_column(data, timetable)
