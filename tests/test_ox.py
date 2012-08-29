import unittest

from opening_hours import is_open

class TestOxfordshireDataset(unittest.TestCase):

    def test_dataset(self):
        lines = open("tests/dataset_oxfordshire_20120829").readlines()
        for line in lines:
            is_open("Mo", "14:00", line)
