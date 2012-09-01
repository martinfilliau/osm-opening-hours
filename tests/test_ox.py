import unittest

from osm_time.opening_hours import OpeningHours

class TestOxfordshireDataset(unittest.TestCase):

    def test_dataset(self):
        # Test with an extract of opening_hours from OSM Oxfordshire
        # Values known to be incorrect have been removed, you can see
        # the complete file (vs. _valid) in the tests/ directory.
        lines = open("tests/dataset_oxfordshire_20120829_valid").readlines()
        for line in lines:
            oh = OpeningHours(line)
            oh.is_open("Mo", "14:00")
