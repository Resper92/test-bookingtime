import unittest
from datetime import datetime, timedelta
from utils import bookings_times_discovery
class TestBookingsTimesDiscovery(unittest.TestCase):

    def setUp(self):
        # Impostazione per i test
        self.trainer_schedule = [
            {"date": datetime(2025, 1, 5).date(), "start_time": datetime(2025, 1, 5, 9, 0).time(), "end_time": datetime(2025, 1, 5, 17, 0).time()}
        ]
        self.bookings = [
            {"datetime_start": datetime(2025, 1, 5, 11, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 14, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 16, 30), "service_id": 1}
        ]
        self.cur_date = datetime(2025, 1, 5).date()
        self.service_durations = {1: 60} 

    def test_no_bookings(self):
        bookings = []
        result = bookings_times_discovery(self.trainer_schedule, bookings, self.cur_date, self.service_durations)
        expected = [(datetime(2025, 1, 5, 9, 0).time(), datetime(2025, 1, 5, 17, 0).time())]
        self.assertEqual(result, expected)

    def test_full_day_booked(self):
        bookings = [
            {"datetime_start": datetime(2025, 1, 5, 9, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 10, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 11, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 12, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 13, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 14, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 15, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 16, 0), "service_id": 1}
        ]
        result = bookings_times_discovery(self.trainer_schedule, bookings, self.cur_date, self.service_durations)
        self.assertEqual(result, [])

    def test_multiple_bookings(self):
        bookings = [
            {"datetime_start": datetime(2025, 1, 5, 11, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 14, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 16, 30), "service_id": 1}
        ]
        result = bookings_times_discovery(self.trainer_schedule, bookings, self.cur_date, self.service_durations)
        expected = [
            (datetime(2025, 1, 5, 9, 0).time(), datetime(2025, 1, 5, 11, 0).time()), 
            (datetime(2025, 1, 5, 12, 0).time(), datetime(2025, 1, 5, 14, 0).time()), 
            (datetime(2025, 1, 5, 15, 0).time(), datetime(2025, 1, 5, 16, 30).time())
        ]
        self.assertEqual(result, expected)


    def test_partial_day_booked(self):
        bookings = [
            {"datetime_start": datetime(2025, 1, 5, 9, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 12, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 1, 5, 15, 0), "service_id": 1}
        ]
        result = bookings_times_discovery(self.trainer_schedule, bookings, self.cur_date, self.service_durations)
        expected = [
            (datetime(2025, 1, 5, 10, 0).time(), datetime(2025, 1, 5, 12, 0).time()),
            (datetime(2025, 1, 5, 13, 0).time(), datetime(2025, 1, 5, 15, 0).time()),
            (datetime(2025, 1, 5, 16, 0).time(), datetime(2025, 1, 5, 17, 0).time())
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
