import unittest
import pandas as pd
import src.data_analysis.bus_speed_analysis as bus_speed_analysis
import src.data_analysis.bus_punctuality_analysis as bus_punctuality_analysis


class TestBusSpeedAnalysis(unittest.TestCase):

    def test_is_close(self):
        self.assertTrue(bus_speed_analysis.is_close(1, 1, 1, 1))
        self.assertFalse(bus_speed_analysis.is_close(1, 1, 1, 2))

    def test_calculate_speed(self):
        self.assertEqual(bus_speed_analysis.calculate_speed(1, 1, 1, 1,
                                                            '2021-01-01 12:00:00',
                                                            '2021-01-01 12:00:01'), 0)
        self.assertEqual(bus_speed_analysis.calculate_speed(1, 1, 1, 1,
                                                            '2021-01-01 12:00:00',
                                                            '2021-01-01 12:00:00'), 0)


class TestBusPunctualityAnalysis(unittest.TestCase):

    def test_calculate_time_difference(self):
        self.assertEqual(bus_punctuality_analysis.calculate_time_difference('12:00:00', '12:00:01'), 1)
        self.assertEqual(bus_punctuality_analysis.calculate_time_difference('12:00:00', '12:00:00'), 0)

    def test_add_column(self):
        data = pd.DataFrame({'Lines': ['1', '2', '3'], 'Lon': [1, 2, 3], 'Lat': [1, 2, 3],
                             'Time': ['12:00:00', '12:00:01', '12:00:02']})
        timetable = pd.DataFrame({'Lines': ['1', '2', '3'], 'Lon': [1, 2, 3], 'Lat': [1, 2, 3],
                                  'Time': ['12:00:00', '12:00:01', '12:00:02']})
        bus_punctuality_analysis.add_delay_column(data, timetable)
        self.assertEqual(timetable['Delay'].tolist(), [0, 0, 0])
