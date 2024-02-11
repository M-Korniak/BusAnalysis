import matplotlib.pyplot as plt
import os
import src.data_analysis.bus_speed_analysis as bus_speed_analysis
import geopandas as gpd


def plot_traffic_on_map(data, path_to_geojson, axs, hour):
    data = data[data['Time'].str.contains(hour)]
    warsaw = gpd.read_file(path_to_geojson)
    warsaw.plot(ax=axs, color='grey')
    axs.scatter(data['Lon'], data['Lat'], s=10)
    axs.set_xlabel('Longitude')
    axs.set_ylabel('Latitude')
    axs.set_title(f'Density of buses at {hour}')


def plot_jammed_places(localizations, axs, axs2, path_to_geojson, hour):
    places = localizations[localizations['All_Buses'] > 10]
    average_speed = places['Average_Speed'].mean()
    places = places.sort_values(by='Average_Speed')
    places = places.head(15)

    warsaw = gpd.read_file(path_to_geojson)
    warsaw.plot(ax=axs, color='lightgrey')
    axs.scatter(places['Lon'], places['Lat'], c=places['Average_Speed'], cmap='coolwarm', s=100)
    axs.set_xlabel('Longitude')
    axs.set_ylabel('Latitude')
    axs.set_title(f'Places with the lowest average speed at {hour}\n'
                  f'Average speed: {average_speed:.2f} km/h')

    places.index = range(len(places))
    axs2.bar(places.index, places['Average_Speed'], color='blue')
    axs2.set_xlabel('Place')
    axs2.set_ylabel('Average speed [km/h]')
    axs2.set_title(f'Ranking of places with the lowest average speed at {hour}\n'
                   f'(Mostly bus depots and traffic jams)')
    axs2.set_xticks(places.index)
    axs2.set_xticklabels([f'{places["Lon"].iloc[i]:.2f}, {places["Lat"].iloc[i]:.2f}'
                          for i in range(len(places))], rotation=45)


def plot_traffic_jam(path='data/buses_localization_16:00.csv',
                     path_to_save='analysis/',
                     path_to_geojson='data/warszawa.geojson'):
    # warszawa.geojson link: https://github.com/andilabs/warszawa-dzielnice-geojson/blob/master/warszawa.geojson
    hour = path.split('_')[-1].split('.')[0]
    data = bus_speed_analysis.bus_speed_analysis(path)
    localizations = bus_speed_analysis.bus_localization_speed(path)

    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    plot_traffic_on_map(data, path_to_geojson, axs[0], hour)
    plot_jammed_places(localizations, axs[1], axs[2], path_to_geojson, hour)

    plt.tight_layout()
    plt.savefig(os.path.join(path_to_save, f'traffic_jam_{hour}.png'))


if __name__ == "__main__":
    plot_traffic_jam()

