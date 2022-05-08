import re

from common_utils import save_local_response, send_get_request
from bs4 import BeautifulSoup


def extract_coords(result_body):
    coords = []
    result_body = str(result_body)

    coords = re.findall(
        'LatLng\("([+-]?[0-9]*[.]?[0-9]+)"\, "([+-]?[0-9]*[.]?[0-9]+)"', result_body
    )

    return coords


def clean_status(status_text):
    sub_text = status_text.replace("Status:", "")
    sub_text = sub_text.replace("\n", "")

    return sub_text


def twelve_to_twenty_four(time):
    # am = true, pm = false
    am_or_pm = None

    if time.find("am") == -1 and time.find("pm") == -1:
        return ("00:00:00", "00:00:00")

    if time.find("am") != -1:
        am_or_pm = True
    else:
        am_or_pm = False

    hour = time.strip("amp")

    if am_or_pm == False:
        if hour == "12":
            hour = 12
        else:
            hour = int(hour) + 12
    else:
        if hour == "12":
            hour = 0

    return "{:02}:00:00".format(int(hour))


def timestamp_conv(timestamp):
    open = ""
    close = ""

    split = timestamp.split("-")

    open = twelve_to_twenty_four(split[0])
    close = twelve_to_twenty_four(split[1])

    return (open, close)


def get_num_rinks(soup):
    span_padding = 7
    result_header = str(soup.find("div", "row result-header"))

    loc_res_span_start = result_header.find("<span>") + span_padding
    loc_res_span_end = result_header.find(" results", loc_res_span_start)

    return int(result_header[loc_res_span_start:loc_res_span_end])


def generate_cambridge_list(soup, total_num):
    list = []
    result_body = soup.findAll("div", "result-body")
    titles = soup.findAll("div", "facility-title")
    addresses = soup.findAll("div", "facility-address")
    hours = soup.findAll("div", "facility-hours")
    statuses = soup.findAll("div", "facility-status")
    latlongs = extract_coords(result_body)

    for i in range(0, total_num):
        name = titles[i].text.strip()
        address = addresses[i].text.strip()
        hour = hours[i].text.strip()
        status = clean_status(statuses[i].text.strip())
        coord = latlongs[i]

        loc_cr = hour.rfind("\n") + 1
        hour = hour[loc_cr:]
        op_hours_ts = timestamp_conv(hour)

        new_rink = {
            "name": name,
            "streetAddress": address,
            "city": "Cambridge",
            "province": "ON",
            "country": "Canada",
            "status": status.upper(),
            "openTime": op_hours_ts[0],
            "closeTime": op_hours_ts[1],
            "latitude": float(coord[0]),
            "longitude": float(coord[1]),
        }

        list.append(new_rink)

    return list


def process_cambridge(url, save):
    res_text = send_get_request(url)

    # Make sure that the GET request didn't return a 404, 500, etc.
    if isinstance(res_text, int) == True:
        exit()

    # for working on local copy of response
    # res_text = open("local_responses/camb.html", "r", encoding="utf-8").read()

    if save == True:
        save_local_response("cambridge", res_text)

    soup = BeautifulSoup(res_text, "html.parser")

    list_items = generate_cambridge_list(soup, get_num_rinks(soup))

    return list_items
