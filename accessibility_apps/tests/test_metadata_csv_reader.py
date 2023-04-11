# ===================================================
# File: test_metadata_csv_reader.py
# Author: Trent Bultsma
# Date: 3/28/2023
# Description: Tests the reading of metadata from a 
#   csv file.
# ==================================================

#! Run This test from the parent directory or module (accessibility_apps) to avoid relative import errors.
# python -m unittest -v tests.test_metadata_csv_reader

import os
import unittest
from utils.harvest.metadata_csv_reader import read_metadata_csv

INPUT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\data\\input"

class MetadataCsvTests(unittest.TestCase):
    """Tests csv metadata reading functions."""

    def test_metadata_csv_reading(self):
        """Test reading the metadata from the csv file"""
        
        # setup the test case
        csv_name = INPUT_DIRECTORY + "/upload_sample.csv"
        test_file_path = "https://s3.us-east-1.amazonaws.com/na-st01.ext.exlibrisgroup.com/01ALLIANCE_WSU/upload/esploro/talea-test/4h_2022_10.pdf"
        expected_test_file_metadata = {
            "ASSET_TITLE" : ["Grant County 4H Update, October 2022"],
            "ASSET_PUBLISHDATE" : ["202210"],
            "ASSET_AVAILDATE" : ["20230301"],
            "ASSET_RESTYPE" : ["publication.newsletterArticle"],
            "ASSET_KEYWORDS" : ["4-H club"],
            "ASSET_PEEREVIEW" : ["NO"],
            "ASSET_LANG" : ["eng"],
            "ASSET_COPYRIGHT" : ["http://rightsstatements.org/vocab/InC/1.0/"],
            "ASSET_AFFILIATION" : ["01ALLIANCE_WSU___41_01_01"],
            "ASSET_FORMAT" : ["pdf"],
            "ASSET_OPENACCESS" : ["YES"],
            "ASSET_DATEEPUB" : ["202210"],
            "ASSET_PORTAL_VISIBILITY" : ["TRUE"],
            "ASSET_PROFILE_VISIBILITY" : ["FALSE"],
            "OCREATOR_ORGANIZATION" : ["Washington State University Extension", "4H Organization", "Creator 3"],
            "FILE_FILEURL" : [test_file_path],
            "FILE_DISPLAY_NAME" : ["Grant County 4H Update, October 2022"]
        }

        # run the function
        overall_metadata_result = read_metadata_csv(csv_name)

        # compare with the expected output
        test_file_metadata = overall_metadata_result[test_file_path]
        for field, value in expected_test_file_metadata.items():
            self.assertEqual(value, test_file_metadata[field])