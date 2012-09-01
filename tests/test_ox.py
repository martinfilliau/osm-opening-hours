import unittest

from opening_hours import OpeningHours

class TestOxfordshireDataset(unittest.TestCase):

    def test_dataset(self):
        lines = open("tests/dataset_oxfordshire_20120829").readlines()
        for line in lines:
            oh = OpeningHours(line)
            oh.is_open("Mo", "14:00")
