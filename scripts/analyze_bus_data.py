import argparse
import os
import src.data_visualization.bus_speed_visualization as bus_speed_visualization
import src.data_visualization.traffic_jam_visualization as traffic_jam_visualization
import src.data_visualization.bus_punctuality_visualization as bus_punctuality_visualization

# Before running this script, make sure that you have the following files in the data/ folder:
# bus_stops.csv, timetable.csv, warszawa.geojson

# Run this
# script in the terminal:
# python scripts/analyze_bus_data.py --path data/buses_location_16:00.csv --output_folder analysis/
# This will visualize the speed of buses and save the visualization in the analysis/ folder


def main():
    parser = argparse.ArgumentParser(description='Visualize bus speed data')

    parser.add_argument('--path', type=str, default='data/buses_location_16:00.csv',
                        help='path to read data from')
    parser.add_argument('--output_folder', type=str, default='analysis/',
                        help='file to save the visualization in')
    args = parser.parse_args()

    hour = args.path.split('_')[-1].split('.')[0]
    new_folder = os.path.join(args.output_folder, f'bus_analysis_{hour}')
    os.makedirs(new_folder, exist_ok=True)
    args.output_folder = new_folder

    bus_speed_visualization.plot_speed_visualization(args.path, new_folder)
    traffic_jam_visualization.plot_traffic_jam(args.path, new_folder)
    bus_punctuality_visualization.plot_bus_punctuality(args.path, new_folder)


if __name__ == '__main__':
    main()
