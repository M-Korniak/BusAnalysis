from src.data_collection import bus_stops
import argparse


# Run this
# script in the terminal:
# python scripts/collect_stops_info.py --folder data/
# This will collect data for bus stops and save it in the data/ folder

def main():
    parser = argparse.ArgumentParser(description='Collect bus localization data')

    parser.add_argument('--folder', type=str, default='data/',
                        help='folder to save data in')

    args = parser.parse_args()

    print("It may take up to 20 minutes to collect data for bus stops")
    bus_stops.get_bus_stops(args.folder)


if __name__ == '__main__':
    main()
    