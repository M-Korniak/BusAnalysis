import argparse
from src.data_collection import bus_localization


# Run this
# script in the terminal:
# python scripts/collect_localization.py 167 197 --minutes 3 --folder data/
# This will collect data for buses 167 and 197 for 3 minutes and save it in the data/ folder

def main():
    parser = argparse.ArgumentParser(description='Collect bus localization data')

    parser.add_argument('bus_numbers', type=str, nargs='+',
                        help='list of bus numbers to collect data for')
    parser.add_argument('--minutes', type=int, default=60,
                        help='how many minutes to collect data for')
    parser.add_argument('--folder', type=str, default='data/',
                        help='folder to save data in')
    args = parser.parse_args()

    bus_localization.get_bus_localization(args.bus_numbers, args.minutes, args.folder)


if __name__ == '__main__':
    main()
