import unittest

from osm_time import get_minutes_from_midnight, clean_value, ParseException
from osm_time.opening_hours import OpeningHours

class TestHelpers(unittest.TestCase):
    
    def test_get_minutes_from_midnight(self):
        self.assertEqual(get_minutes_from_midnight("0:00"), 0)
        self.assertEqual(get_minutes_from_midnight("02:00"), 120)
        self.assertEqual(get_minutes_from_midnight("18:42"), 1122)

    def test_clean_value(self):
        self.assertEqual(clean_value("Mo-Fr 08:30-22:00; "), "mo-fr 08:30-22:00")

    def test_parse_exception(self):
        self.assertRaises(ParseException, OpeningHours, "sunrise-sunset")


if __name__ == "__main__":
    unittest.main()
