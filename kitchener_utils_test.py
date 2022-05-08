import unittest
import difflib

from bs4 import BeautifulSoup
from common_utils import send_get_request
from kitchener_utils import extract_lat_long, get_long_url

class Test(unittest.TestCase):
    url = "https://www.kitchener.ca/en/recreation-and-sports/outdoor-skating-rinks.aspx"
    response = send_get_request(url)

    def test_get_long_url(self):
        short_url = "https://goo.gl/maps/VELNcAbL3Du41T7SA"
        long_url = "https://www.google.com/maps/place/Ahrens+St+E,+Kitchener,+ON+N2H+2H1/@43.4530397,-80.4864701,368m/data=!3m1!1e3!4m5!3m4!1s0x882bf492de1a25ed:0xdfed74c446269426!8m2!3d43.4528681!4d-80.4854237?shorturl=1"
        test_url = ""   
        
        test_url = get_long_url(short_url)

        ratio = difflib.SequenceMatcher(None, long_url, test_url).ratio()
        self.assertTrue(ratio >= 0.95)

    def test_extract_lat_long(self):
        test_coords = ['43.439163', '-80.506289']

        loc_of_list_heading = self.response.index('a name="locations"')
        loc_of_list = self.response.find("<ul>", loc_of_list_heading)
        loc_end_of_list = self.response.find("</ul>", loc_of_list_heading) + 5
    
        subdata = self.response[loc_of_list:loc_end_of_list]

        lis = BeautifulSoup(subdata, "html.parser").find_all("li")

        coords = extract_lat_long(lis[0])
        self.assertEqual(test_coords[0], coords[0])
        self.assertEqual(test_coords[1], coords[1])


if __name__ == "__main__":
    unittest.main()
