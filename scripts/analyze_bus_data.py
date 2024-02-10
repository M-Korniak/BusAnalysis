import argparse
import src.data_visualization.bus_speed_visualization as bus_speed_visualization
import src.data_visualization.traffic_jam_visualization as traffic_jam_visualization


# Run this
# script in the terminal:
# python scripts/analyze_bus_data.py --path data/buses_localization_16:00.csv --output_folder analysis/
# This will visualize the speed of buses and save the visualization in the analysis/ folder

def main():
    parser = argparse.ArgumentParser(description='Visualize bus speed data')

    parser.add_argument('--path', type=str, default='data/buses_localization_16:00.csv',
                        help='path to read data from')
    parser.add_argument('--output_folder', type=str, default='analysis/',
                        help='file to save the visualization in')
    args = parser.parse_args()

    bus_speed_visualization.plot_speed_visualization(args.path, args.output_folder)
    traffic_jam_visualization.plot_traffic_jam(args.path, args.output_folder)


if __name__ == '__main__':
    main()
