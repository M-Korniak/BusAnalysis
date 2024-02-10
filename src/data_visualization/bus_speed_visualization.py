import matplotlib.pyplot as plt
import src.data_analysis.bus_speed_analysis as bus_speed_analysis
import geopandas as gpd


def plot_buses_speed_distribution(data, axs):
    axs.hist(data['Speed'], bins=30, range=(0, 100), color='blue', edgecolor='black')
    axs.set_xlabel('Speed [km/h]')
    axs.set_ylabel('Number of measurements')
    axs.set_title('Speed distribution of buses')


def plot_fast_buses(data, axs):
    vehicle_max_speed = data.groupby('VehicleNumber')['Speed'].max()
    fast_vehicles = vehicle_max_speed[vehicle_max_speed > 50]
    percentage = len(fast_vehicles) / len(vehicle_max_speed) * 100

    fast_buses = data[data['Speed'] > 50]

    axs.hist(fast_buses['Speed'], bins=30, range=(50, 100), color='red', edgecolor='black')
    axs.set_xlabel('Speed [km/h]')
    axs.set_ylabel('Number of measurements')
    axs.set_title(f'Total {len(fast_buses)} measurements with speed > 50 km/h\n'
                  f'({percentage:.2f}% of all buses at some point had speed > 50 km/h)')


def plot_places_with_fast_buses(localizations, axs, axs2, path_to_geojson):
    fast_place = localizations[localizations['All_Buses'] > 10]
    fast_place = fast_place.sort_values(by='Fast_Percentage', ascending=False)

    fast_place = fast_place.head(10)

    warsaw = gpd.read_file(path_to_geojson)
    warsaw.plot(ax=axs, color='lightgrey')
    axs.scatter(fast_place['Lon'], fast_place['Lat'], c=fast_place['Fast_Percentage'], cmap='coolwarm', s=100)
    axs.set_xlabel('Longitude')
    axs.set_ylabel('Latitude')
    axs.set_title('Places with the highest percentage of fast buses')
    for i in range(len(fast_place)):
        axs.text(fast_place['Lon'].iloc[i], fast_place['Lat'].iloc[i],
                 f'{100 * fast_place["Fast_Percentage"].iloc[i]:.2f}%', fontsize=7, ha='center')

    fast_place.index = range(len(fast_place))
    axs2.bar(fast_place.index, fast_place['Fast_Percentage'] * 100, color='blue')
    axs2.set_xlabel('Place')
    axs2.set_ylabel('Percentage of fast buses')
    axs2.set_title('Ranking of places with the highest percentage of fast buses')
    axs2.set_xticks(fast_place.index)
    axs2.set_xticklabels([f'{fast_place["Lon"].iloc[i]:.2f}, {fast_place["Lat"].iloc[i]:.2f}'
                          for i in range(len(fast_place))], rotation=45)


def plot_speed_visualization(path='/Users/michalkorniak/Documents/Programs/Python/'
                                  'PycharmProjects/BusAnalysis/data/buses_localization_16:00.csv',
                             path_to_save='/Users/michalkorniak/Documents/Programs/Python/'
                                          'PycharmProjects/BusAnalysis/analysis/',
                             path_to_geojson='/Users/michalkorniak/Documents/Programs/Python/'
                                             'PycharmProjects/BusAnalysis/data/warszawa.geojson'):
    # warszawa.geojson link: https://github.com/andilabs/warszawa-dzielnice-geojson/blob/master/warszawa.geojson

    # take hour from path
    hour = path.split('_')[-1].split('.')[0]
    data = bus_speed_analysis.bus_speed_analysis(path)
    localizations = bus_speed_analysis.bus_localization_speed(path)

    fig, axs = plt.subplots(4, 1, figsize=(10, 15))

    plot_buses_speed_distribution(data, axs[0])
    plot_fast_buses(data, axs[1])
    plot_places_with_fast_buses(localizations, axs[2], axs[3], path_to_geojson)

    plt.tight_layout()
    plt.savefig(f'{path_to_save}buses_speed_distribution_{hour}.png')


