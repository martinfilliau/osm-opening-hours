import unittest

from opening_hours import is_open

class TestOpeningDays(unittest.TestCase):

    def test_twenty_four_seven(self):
        time = "15:00"
        day = "Mo"
        value = "24/7"
        self.assertEqual(is_open(day, time, value), True)

    def test_parse_one_day(self):
        day = "Mo"
        value = "Mo 10:00-16:00"
        self.assertEqual(is_open(day, "15:00", value), True)
        self.assertEqual(is_open(day, "18:00", value), False)

    def test_parse_value(self):
        time = "12:00"
        day = "Mo"
        value = "Mo-Fr 08:30-20:00"
        self.assertEqual(is_open(day, time, value), True)

    def test_complex_value(self):
        value = "Mo 10:00-12:00,12:30-15:00; Tu-Fr 08:00-12:00,12:30-15:00; Sa 08:00-12:00"
        self.assertEqual(is_open("Su", "10:00", value), False)
        self.assertEqual(is_open("Mo", "10:30", value), True)
        self.assertEqual(is_open("We", "14:00", value), True)
        self.assertEqual(is_open("Sa", "14:00", value), False)

if __name__ == "__main__":
    unittest.main()
