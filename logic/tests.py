import unittest
import os
import re

import ray
from fuzzywuzzy import fuzz

from data_extractor import *

import unittest

import pandas as pd


# ['File_name', 'airplane_title', 'max_speed_kmph', 'error', 'range_km']

class TestDataframeCSV(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.df = pd.read_csv("final_result_sequential.csv")

    def test_columns_present(self):
        """ensures that the expected columns are all present"""
        self.assertIn("File_name", self.df.columns)
        self.assertIn("airplane_title", self.df.columns)
        self.assertIn("max_speed_kmph", self.df.columns)
        self.assertIn("error", self.df.columns)
        self.assertIn("range_km", self.df.columns)

    def test_non_empty(self):
        """ensures that there is more than one row of data"""
        self.assertNotEqual(len(self.df.index), 0)

    def test_data_correct(self):
        """ensures there is no unexpected data in columns"""
        print(self.df.dtypes)

        assert self.df.dtypes['max_speed_kmph'] == int, "should be int"



unittest.main()
