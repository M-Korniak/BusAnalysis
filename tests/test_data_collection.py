import unittest
from unittest.mock import mock_open, patch
import src.data_collection.bus_localization as bus_localization
import src.data_collection.bus_stops as bus_stops


class TestBusLocalization(unittest.TestCase):
    @patch('src.data_collection.bus_localization.time')
    @patch('src.data_collection.bus_localization.requests')
    def test_get_bus_localization(self, mock_requests, mock_time):
        mock_time.strftime.return_value = '12:00'
        mock_requests.get.return_value.json.return_value = {'result': 'Błędna metoda lub parametry wywołania'}
        mock_time.sleep.return_value = None
        with patch('builtins.open', mock_open()) as mock_file:
            bus_localization.get_bus_localization(1)
            mock_file.assert_called_once_with('data/buses_localization_12:00.csv', 'w')


class TestBusStops(unittest.TestCase):
    @patch('src.data_collection.bus_stops.requests')
    def test_timetable_at_stop(self, mock_requests):
        mock_requests.get.return_value.json.return_value = {'result': [{'values': [{'value': '12:00', 'key': 'czas'}]}]}
        with patch('builtins.open', mock_open()) as mock_file:
            bus_stops.timetable_at_stop([{'stop_id': 1, 'stop_nr': 1, 'line': 1}])
            mock_file.assert_called_once_with('data/timetable.csv', 'w')
