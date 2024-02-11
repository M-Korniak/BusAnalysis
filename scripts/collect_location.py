import argparse
from src.data_collection import bus_location


# Run this
# script in the terminal:
# python scripts/collect_location.py --minutes 60 --folder data/
# This will collect data for buses for 60 minutes and save it in the data/ folder

def main():
    parser = argparse.ArgumentParser(description='Collect bus localization data')

    parser.add_argument('--minutes', type=int, default=60,
                        help='how many minutes to collect data for')
    parser.add_argument('--folder', type=str, default='data/',
                        help='folder to save data in')
    args = parser.parse_args()

    bus_location.get_bus_location(args.minutes, args.folder)


if __name__ == '__main__':
    main()
