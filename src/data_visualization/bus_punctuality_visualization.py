import matplotlib.pyplot as plt
import os
import geopandas as gpd
import src.data_analysis.bus_punctuality_analysis as bus_punctuality_analysis


def plot_punctuality_distribution(data, axs):
    axs.hist(data['Delay'], bins=30, range=(0, 30), color='blue', edgecolor='black')
    axs.set_xlabel('Delay / Ahead of time [min]')
    axs.set_ylabel('Number of measurements')
    axs.set_title('Delay / Ahead of time distribution of buses\n'
                  'Mean delay / Ahead of time: {:.2f} min'.format(data['Delay'].mean()))


def plot_how_many_on_time(data, axs):
    on_time = data[data['Delay'] <= 1]
    late = data[data['Delay'] > 1]
    axs.bar(['On time (Delay <= 1)', 'Late (Delay >= 1)'], [len(on_time), len(late)], color='blue')
    axs.set_xlabel('Bus status')
    axs.set_ylabel('Number of buses')
    axs.set_title('How many buses are on time?\n'
                  'On time: {:.2f}%'.format(len(on_time) / len(data) * 100))


def plot_stops_punctuality(data, axs, axs2, path_to_geojson):
    data = data.groupby(['Stop_Id', 'Stop_Nr']).agg({'Delay': 'mean', 'Lon': 'min', 'Lat': 'min'}).reset_index()
    data = data.sort_values(by='Delay', ascending=False).head(15)
    warsaw = gpd.read_file(path_to_geojson)
    warsaw.plot(ax=axs, color='lightgrey')
    axs.scatter(data['Lon'], data['Lat'], c=data['Delay'], cmap='coolwarm', s=100)
    axs.set_xlabel('Longitude')
    axs.set_ylabel('Latitude')
    axs.set_title('Bus stops with the most delay')

    data.index = range(len(data))
    axs2.bar(data.index, data['Delay'], color='red')
    axs2.set_xlabel('Stop')
    axs2.set_ylabel('Mean delay [min]')
    axs2.set_title('Ranking of bus stops with the most delay')
    axs2.set_xticks(data.index)
    axs2.set_xticklabels([f'{data["Lon"].iloc[i]:.2f}, {data["Lat"].iloc[i]:.2f}'
                          for i in range(len(data))], rotation=45)


def plot_bus_punctuality(path='data/buses_localization_16:00.csv',
                         path_to_save='analysis/',
                         path_to_geojson='data/warszawa.geojson',
                         path_to_bus_stops='data/bus_stops.csv',
                         path_to_timetable='data/timetable.csv'):
    # warszawa.geojson link: https://github.com/andilabs/warszawa-dzielnice-geojson/blob/master/warszawa.geojson
    data = bus_punctuality_analysis.bus_stops_punctuality(path, path_to_bus_stops, path_to_timetable)

    data = data.dropna()
    # Drop delay > 30 minutes
    data = data[data['Delay'] < 30 * 60]
    data['Delay'] = data['Delay'] / 60.0
    data.reset_index(drop=True, inplace=True)

    fig, axs = plt.subplots(4, 1, figsize=(10, 15))

    plot_punctuality_distribution(data, axs[0])
    plot_how_many_on_time(data, axs[1])
    plot_stops_punctuality(data, axs[2], axs[3], path_to_geojson)

    plt.tight_layout()
    plt.savefig(os.path.join(path_to_save, 'bus_punctuality.png'))
