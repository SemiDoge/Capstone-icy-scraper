import unittest
import difflib
import os
import json

from bs4 import BeautifulSoup

from cambridge_utils import generate_cambridge_list, get_num_rinks
from common_utils import *


class Test(unittest.TestCase):
    url = "https://facilities.cambridge.ca/?CategoryIds=82&FacilityTypeIds="
    response = ""

    def test_send_get_request(self):
        self.response = send_get_request(self.url)
        self.assertTrue(isinstance(self.response, str))

    def test_jsonify_city(self):
        # fmt: off
        example_list = []
        example_list.append({'name': 'Angewood Park Outdoor Rink', 'streetAddress': '120 Angela Crescent, Cambridge, N1S 4B6', 'city': 'Cambridge', 'province': 'ON', 'country': 'Canada', 'status': 'CLOSED FOR THE SEASON', 'openTime': '07:00:00', 'closeTime': '22:00:00', 'latitude': 43.3416748046875, 'longitude': -80.3403854370117})
        example_list.append({'name': 'Can-Amera Park Outdoor Rink', 'streetAddress': '305 Saginaw Parkway, Cambridge', 'city': 'Cambridge', 'province': 'ON', 'country': 'Canada', 'status': 'CLOSED FOR THE SEASON', 'openTime': '07:00:00', 'closeTime': '21:00:00', 'latitude': 43.3899574279785, 'longitude': -80.2942504882813})
        example_list.append({'name': 'Domm Park Outdoor Rink', 'streetAddress': '55 Princess St.', 'city': 'Cambridge', 'province': 'ON', 'country': 'Canada', 'status': 'CLOSED FOR THE SEASON', 'openTime': '07:00:00', 'closeTime': '22:00:00', 'latitude': 43.3712882995605, 'longitude': -80.3427352905273})


        jsun = jsonify_city(example_list) 
        
        self.assertTrue(isinstance(jsun, str))

    def test_save_local_response(self):
        filename = "cambridge"
        response = send_get_request(self.url)


        platform_indep_delete("local_responses")
        save_local_response(filename, response)

        local_responses = [f for f in os.listdir('./local_responses') if f.endswith('.html')]
        self.assertTrue(len(local_responses) == 1)


        filename = local_responses[0]

        with open("local_responses/{}".format(filename), "r", encoding="utf-8") as f:
            local_copy = f.read()


        ratio = difflib.SequenceMatcher(None, response, local_copy).ratio()
        self.assertTrue(ratio >= 0.85)

        # self.assertTrue(local_copy == response)

    def test_save_scraped_data(self):
        filename = "cambridge"
        response = send_get_request(self.url)

        soup = BeautifulSoup(response , "html.parser")
        data = generate_cambridge_list(soup, get_num_rinks(soup))

        jsun = jsonify_city(data)

        platform_indep_delete("scraped_data")

        save_scraped_data(filename, jsun)
        scraped_data_dir = [f for f in os.listdir('./scraped_data') if f.endswith('.json')]
        self.assertTrue(len(scraped_data_dir) == 1)

        filename = scraped_data_dir[0]

        with open("scraped_data/{}".format(filename), "r", encoding="UTF-8") as f:
            local_scrape = f.read()

        scrape = json.loads(local_scrape)

        self.assertTrue(len(scrape['rinks']) > 2)

if __name__ == "__main__":
    unittest.main()
