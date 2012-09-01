import unittest

from osm_time.opening_hours import OpeningHours, ParseException
from osm_time.opening_hours import get_minutes_from_midnight, clean_value, process_time_range

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

    def test_day_off(self):
        oh = OpeningHours("Mo-Sa 09:30-20:45; Su off;")
        self.assertEqual(oh.is_open("Fr", "20:44"), True)
        self.assertEqual(oh.is_open("su", "12:00"), False)

    def test_complex_value(self):
        oh = OpeningHours("Mo 10:00-12:00,12:30-15:00; Tu-Fr 08:00-12:00,12:30-15:00; Sa 08:00-12:00; PH 09:00-11:30;")
        self.assertEqual(oh.is_open("Su", "10:00"), False)
        self.assertEqual(oh.is_open("Mo", "10:30"), True)
        self.assertEqual(oh.is_open("Mo", "12:15"), False)
        self.assertEqual(oh.is_open("We", "14:00"), True)
        self.assertEqual(oh.is_open("Sa", "14:00"), False)
        self.assertEqual(oh.is_open("ph", "10:00"), True)

    def test_complex_value_minutes(self):
        oh = OpeningHours("Mo 10:00-12:00,12:30-15:00; Tu-Fr 08:00-12:00,12:30-15:00; Sa 08:00-12:00")
        self.assertEqual(oh.minutes_to_closing("Su", "10:00"), 0)
        self.assertEqual(oh.minutes_to_closing("Mo", "10:30"), 90)
        self.assertEqual(oh.minutes_to_closing("Mo", "12:15"), 0)
        self.assertEqual(oh.minutes_to_closing("We", "14:00"), 60)
        self.assertEqual(oh.minutes_to_closing("Sa", "14:00"), 0)

    def test_get_minutes_from_midnight(self):
        self.assertEqual(get_minutes_from_midnight("0:00"), 0)
        self.assertEqual(get_minutes_from_midnight("02:00"), 120)
        self.assertEqual(get_minutes_from_midnight("18:42"), 1122)

    def test_clean_value(self):
        self.assertEqual(clean_value("Mo-Fr 08:30-22:00; "), "mo-fr 08:30-22:00")

    def test_process_time_range(self):
        self.assertEqual(process_time_range("09:00-20:30"), (540, 1230))
        self.assertEqual(process_time_range("0:00-23:59"), (0, 1439))

    def test_parse_exception(self):
        self.assertRaises(ParseException, OpeningHours, "sunrise-sunset")


if __name__ == "__main__":
    unittest.main()
