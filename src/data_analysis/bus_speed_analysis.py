from functools import cache
import pandas as pd
import numpy as np
import datetime


def calculate_speed(lon1, lat1, lon2, lat2, time1, time2):
    # https://en.wikipedia.org/wiki/Haversine_formula
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    lon_len = lon2 - lon1
    lat_len = lat2 - lat1
    a = np.sin(lat_len / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon_len / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    km = 6371 * c

    time1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    time2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
    time = (time2 - time1).total_seconds() / 3600

    if time == 0:
        return 0

    return km / time


@cache
def bus_speed_analysis(path='data/buses_location_16:00.csv'):
    data = pd.read_csv(path, dtype={'Lines': str, 'VehicleNumber': str, 'Time': str, 'Lon': float, 'Lat': float})
    buses_speed = []
    for i in range(len(data) - 1):
        if data['VehicleNumber'][i] == data['VehicleNumber'][i + 1]:
            speed = calculate_speed(data['Lon'][i], data['Lat'][i], data['Lon'][i + 1],
                                    data['Lat'][i + 1], data['Time'][i], data['Time'][i + 1])
            buses_speed.append(speed)
        else:
            speed = buses_speed[-1]
            buses_speed.append(speed)

    buses_speed.append(buses_speed[-1])
    data['Speed'] = buses_speed

    return data


def is_close(lon1, lat1, lon2, lat2, meters=500):
    # https://en.wikipedia.org/wiki/Haversine_formula
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    lon_len = lon2 - lon1
    lat_len = lat2 - lat1
    a = np.sin(lat_len / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon_len / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    distance = 6371 * c * 1000

    return distance < meters


@cache
def bus_localization_speed(path='data/buses_location_16:00.csv'):
    data = bus_speed_analysis(path)
    data = data.sample(frac=0.07, random_state=1)
    data.index = range(len(data))
    close_points = []
    points_buses_count = {}
    points_fast_buses = {}
    average_speed = {}
    for i in range(len(data)):
        for j in range(len(close_points)):
            if is_close(data['Lon'][i], data['Lat'][i], close_points[j][0], close_points[j][1]):
                points_buses_count[close_points[j]] += 1
                average_speed[close_points[j]] += data['Speed'][i]
                if data['Speed'][i] > 50:
                    points_fast_buses[close_points[j]] += 1
                break
        else:
            close_points.append((data['Lon'][i], data['Lat'][i]))
            points_buses_count[close_points[-1]] = 1
            average_speed[close_points[-1]] = data['Speed'][i]
            if data['Speed'][i] > 50:
                points_fast_buses[close_points[-1]] = 1
            else:
                points_fast_buses[close_points[-1]] = 0

    for point in average_speed:
        average_speed[point] /= points_buses_count[point]

    return pd.DataFrame({'Lon': [close_points[i][0] for i in range(len(close_points))],
                         'Lat': [close_points[i][1] for i in range(len(close_points))],
                         'Fast_Percentage': [points_fast_buses[close_points[i]] / points_buses_count[close_points[i]]
                                             for i in range(len(close_points))],
                         'All_Buses': [points_buses_count[close_points[i]] for i in range(len(close_points))],
                         'Average_Speed': [average_speed[close_points[i]] for i in range(len(close_points))]})
