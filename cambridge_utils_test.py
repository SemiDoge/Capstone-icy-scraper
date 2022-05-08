import unittest
import os

from sys import platform
from bs4 import BeautifulSoup

from cambridge_utils import *
from common_utils import *


class Test(unittest.TestCase):
    url = "https://facilities.cambridge.ca/?CategoryIds=82&FacilityTypeIds="
    response = send_get_request(url)

    def test_extract_coords(self):
        coords = []
        soup = BeautifulSoup(self.response, "html.parser")
        result_body = soup.findAll("div", "result-body")

        coords = extract_coords(result_body)
        self.assertTrue(len(coords) > 2)

    def test_twelve_to_twenty_four(self):
        self.assertEqual("00:00:00", twelve_to_twenty_four("12am"))
        self.assertEqual("01:00:00", twelve_to_twenty_four("1am"))
        self.assertEqual("07:00:00", twelve_to_twenty_four("7am"))
        self.assertEqual("12:00:00", twelve_to_twenty_four("12pm"))
        self.assertEqual("18:00:00", twelve_to_twenty_four("6pm"))
        self.assertEqual("23:00:00", twelve_to_twenty_four("11pm"))

    # test_def_timestamp_conv is covered twelve_to_twenty_four

    def test_clean_status(self):
        dirty = "Status:\n\n\n\nClosed for the season"
        clean = "Closed for the season"

        self.assertEqual(clean, clean_status(dirty))

    def test_get_num_rinks(self):
        soup = BeautifulSoup(self.response, "html.parser")

        self.assertEqual(6, get_num_rinks(soup))


if __name__ == "__main__":
    unittest.main()
