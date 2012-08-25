import unittest

from opening_hours.opening_times import check_time, get_minutes_from_midnight

class TestOpeningHours(unittest.TestCase):

    def test_check_time_inside(self):
        time = "12:00"
        value = "09:00-18:00"
        self.assertEqual(check_time(time, value), True)

    def test_check_time_outside(self):
        time = "19:00"
        value = "09:00-18:00"
        self.assertEqual(check_time(time, value), False)

    def test_check_time_boundary(self):
        time = "12:00"
        value = "09:00-12:00"
        self.assertEqual(check_time(time, value), True)

    def test_minutes_from_midnight_noon(self):
        time = "12:00"
        self.assertEqual(get_minutes_from_midnight(time), 720)

    def test_minutes_from_midnight_midnight(self):
        time = "00:00"
        self.assertEqual(get_minutes_from_midnight(time), 0)

    def test_minutes_from_midnight_more(self):
        time = "25:25"  # TODO validation?
        self.assertEqual(get_minutes_from_midnight(time), 1525)

if __name__ == "__main__":
    unittest.main()
