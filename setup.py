#!/usr/bin/env python

from setuptools import setup 

setup(name='osm_opening_hours',
      version='0.1',
      description='Tools to parse opening hours format from OpenStreetMap.',
      author='Martin Filliau',
      author_email='martin@filliau.com',
      url='https://github.com/martinfilliau/osm-opening-hours',
      py_modules=['osm_time', 'osm_time.opening_hours'],
      classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
      test_suite = "tests",
     )
