import requests
import re

from bs4 import BeautifulSoup
from common_utils import save_local_response, send_get_request


def extract_lat_long(rink_li):
    raw_url = rink_li.find("a")

    if raw_url != None:
        raw_url = raw_url["href"]
    else:
        return [0.00, 0.00]

    if raw_url.find("goo.gl") != -1:
        url = get_long_url(raw_url)
        re_coords = re.findall("(-?\d+\.\d+),*(-?\d+\.\d+)", url)
        return re_coords[0]
    else:
        url = raw_url

    coords = re.findall("(-?\d+\.\d+),*(-?\d+\.\d+)", url)

    claire = re.findall("Clair", url)

    if len(claire) != 0:
        return [0.00, 0.00]

    return coords[0]


def get_long_url(url):
    r = requests.get(url)

    return r.request.url


def generate_kitchener_list(res_text, rinks_cnt):
    list = []
    loc_cur = 0
    lis = BeautifulSoup(res_text, "html.parser").find_all("li")

    # TODO: Time premitting re-write this function using BeautifulSoup
    for i in range(0, rinks_cnt):
        loc_li = res_text.find("<li>", loc_cur) + 4
        loc_end_li = res_text.find("</li>", loc_li)
        loc_cur = loc_end_li

        substring = res_text[loc_li:loc_end_li]

        # extracting name
        first_comma = substring.find(",")
        name = substring[:first_comma]

        # extracting address
        loc_blank = substring.rfind(r'blank">')

        if loc_blank != -1:
            loc_blank += 7
        else:
            loc_blank = substring.find(r",") + 2

        loc_end_addr = substring.find(r"</a>")
        address = substring[loc_blank:loc_end_addr]

        coords = extract_lat_long(lis[i])

        # new_rink = Rink(name, address, "Kitchener", "ON", "Canada")
        new_rink = {
            "name": name,
            "streetAddress": address,
            "city": "Kitchener",
            "province": "ON",
            "country": "Canada",
            "latitude": float(coords[0]),
            "longitude": float(coords[1]),
        }

        list.append(new_rink)

    return list


def process_kitchener(url, save):
    res_text = send_get_request(url)

    if isinstance(res_text, int) == True:
        exit()

    if save == True:
        save_local_response("kitchener", res_text)

    # for working on local copy of response
    # res_text = open("local_responses/kitch.html", "r").read()

    loc_of_list_heading = res_text.index('a name="locations"')
    loc_of_list = res_text.find("<ul>", loc_of_list_heading)
    loc_end_of_list = res_text.find("</ul>", loc_of_list_heading) + 5

    subdata = res_text[loc_of_list:loc_end_of_list]

    list_items = generate_kitchener_list(subdata, subdata.count("<li>"))

    return list_items
