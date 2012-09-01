import unittest

from opening_hours import OpeningHours, ParseException

class TestOpeningDays(unittest.TestCase):

    def test_twenty_four_seven(self):
        oh = OpeningHours("24/7")
        self.assertEqual(oh.is_open("Mo", "15:00"), True)

    def test_parse_one_day(self):
        oh = OpeningHours("Mo 10:00-16:00")
        self.assertEqual(oh.is_open("Mo", "15:00"), True)
        self.assertEqual(oh.is_open("Mo", "18:00"), False)

    def test_we_24(self):
        oh = OpeningHours("Sa-Su 00:00-24:00")
        self.assertEqual(oh.is_open("Sa", "13:00"), True)
        self.assertEqual(oh.is_open("Mo", "06:00"), False)

    def test_parse_multiple_days(self):
        oh = OpeningHours("Mo-Fr 08:30-20:00")
        self.assertEqual(oh.is_open("Mo", "12:00"), True)
        self.assertEqual(oh.is_open("Tu", "12:00"), True)
        self.assertEqual(oh.is_open("Fr", "12:00"), True)
        self.assertEqual(oh.is_open("Su", "12:00"), False)

    def test_complex_value(self):
        oh = OpeningHours("Mo 10:00-12:00,12:30-15:00; Tu-Fr 08:00-12:00,12:30-15:00; Sa 08:00-12:00")
        self.assertEqual(oh.is_open("Su", "10:00"), False)
        self.assertEqual(oh.is_open("Mo", "10:30"), True)
        self.assertEqual(oh.is_open("Mo", "12:15"), False)
        self.assertEqual(oh.is_open("We", "14:00"), True)
        self.assertEqual(oh.is_open("Sa", "14:00"), False)

    def test_complex_value_minutes(self):
        oh = OpeningHours("Mo 10:00-12:00,12:30-15:00; Tu-Fr 08:00-12:00,12:30-15:00; Sa 08:00-12:00")
        self.assertEqual(oh.minutes_to_closing("Su", "10:00"), 0)
        self.assertEqual(oh.minutes_to_closing("Mo", "10:30"), 90)
        self.assertEqual(oh.minutes_to_closing("Mo", "12:15"), 0)
        self.assertEqual(oh.minutes_to_closing("We", "14:00"), 60)
        self.assertEqual(oh.minutes_to_closing("Sa", "14:00"), 0)

    def test_sunrise_sunset(self):
        with self.assertRaises(ParseException):
            oh = OpeningHours("sunrise-sunset")

if __name__ == "__main__":
    unittest.main()
