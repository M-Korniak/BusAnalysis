import argparse
from src.data_collection import bus_localization


# Run this
# script in the terminal:
# python scripts/collect_localization.py --minutes 60 --folder data/
# This will collect data for buses for 60 minutes and save it in the data/ folder

def main():
    parser = argparse.ArgumentParser(description='Collect bus localization data')

    parser.add_argument('--minutes', type=int, default=60,
                        help='how many minutes to collect data for')
    parser.add_argument('--folder', type=str, default='data/',
                        help='folder to save data in')
    args = parser.parse_args()

    bus_localization.get_bus_localization(args.minutes, args.folder)


if __name__ == '__main__':
    main()
