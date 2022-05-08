import warnings
import requests
import json

from bs4 import BeautifulSoup

from common_utils import save_local_response, send_get_request


# [{name: "", address: ""} ..]
def format_list(ul):
    all_parks_list = []

    # Clean leftover html tags and other assorted junk from the data
    cleaned_list = list(
        filter(
            lambda val: (
                not str(val).startswith("<")
                and val != "\n"
                and not str(val).startswith(" ")
                and not str(val).startswith("\xa0")
                and not str(val).startswith("(")
                and not str(val).startswith(",")
                # The following parks have no ice rink and also don't provide an address
                and not (val == "RIM Park")
                and not (val == "Hillside Park")
                and not (val == "Waterloo Park")
                and not (val == "Bechtel Park")
            ),
            ul,
        )
    )

    address = 1
    for name in range(0, len(cleaned_list), 2):
        new_park = {
            "name": cleaned_list[name].replace(",", "").replace("(", "").strip(),
            "address": cleaned_list[address],
        }

        all_parks_list.append(new_park)
        address += 2

    return all_parks_list


def gather_addresses_parks_dir(soup):
    accordion = soup.findAll("table", "icrtAccordion")
    accordionSoup = BeautifulSoup(str(accordion), "html.parser")

    ul = accordionSoup.findAll("ul")[0]
    tex = list(ul.descendants)

    return format_list(tex)


def fields_dir_combine(ustr):
    new_combined_ustr = ""

    ustr = ustr.replace("<ul>", "", 4)
    ustr = ustr.replace("</ul>", "", 5)

    new_combined_ustr = "<ul>{}</ul>".format(ustr)

    return new_combined_ustr


def listify_fields(ul):
    fields_list = set()
    ul_soup = BeautifulSoup(ul, "html.parser")
    lis = ul_soup.select("li")

    for li in lis:
        name = li.text.rsplit(",")[0]
        address = li.text.rsplit(",")[1].replace("\xa0", "")

        new_park = {"name": name, "address": address}

        fields_list.add(json.dumps(new_park))

    # remove duplicates
    fields_list = list(dict.fromkeys(fields_list))

    for li in range(0, len(fields_list)):
        fields_list[li] = json.loads(fields_list[li])

    # print(json.loads(fields_list[0])["name"])
    # print(fields_list[0]["name"])

    return fields_list


def gather_addresses_fields_dir(soup):
    accordion = soup.findAll("table", "icrtAccordion")
    accordionSoup = BeautifulSoup(str(accordion), "html.parser")

    ul = accordionSoup.findAll("ul")

    full_ul = ""

    for i in range(0, len(ul)):
        full_ul += str(ul[i])

    full_ul = fields_dir_combine(full_ul)

    return listify_fields(full_ul)


def get_num_rinks(soup):

    ul = soup.find_all("a", attrs={"name": "community-rink-hours"})[0].find_next("ul")
    rinks_count = ul.text.strip().count("\n") + 1

    return int(rinks_count)


def waterloo_workaround_get_request(url):

    warnings.filterwarnings("ignore")
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
            "HIGH:!DH:!aNULL"
        )
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

    res = send_get_request(url)

    if isinstance(res, int) == True:
        exit()

    return res


def try_parks_dir_for_address(name, parks_info):

    # print(parks_info)

    j = next(
        (j for j, item in enumerate(parks_info) if item["name"].find(name) != -1),
        None,
    )

    if j == None:
        address = "Unknown"
    else:
        address = parks_info[j]["address"]

    return address


def generate_waterloo_list(soup, loc_soup, fields_soup, total_num):
    list = []
    address_info = []
    all_ul = soup.findAll("ul")
    rink_titles = (
        soup.find_all("a", attrs={"name": "community-rink-hours"})[0]
        .find_next("ul")
        .find_all("li")
    )

    address_info = gather_addresses_parks_dir(loc_soup)
    parks_info = gather_addresses_fields_dir(fields_soup)

    # print("{} = {}".format(address_info[0]["name"], parks_info[0]["name"]))

    # let's start with the Public Square Rink first

    if soup.find("a", attrs={"name": "waterloo-public-square-rink"}) != None:
        public_sq = {
            "name": "Public Square",
            "streetAddress": "75 King Street South",
            "city": "Waterloo",
            "province": "ON",
            "country": "Canada",
        }

    list.append(public_sq)

    for i in range(0, total_num):
        name = rink_titles[i].text.replace("\xa0", " ").strip()

        j = next(
            (j for j, item in enumerate(address_info) if item["name"].find(name) != -1),
            None,
        )

        if j == None:
            address = try_parks_dir_for_address(name, parks_info)
        else:
            address = address_info[j]["address"]

        new_rink = {
            "name": name,
            "streetAddress": address,
            "city": "Waterloo",
            "province": "ON",
            "country": "Canada",
            # "schedule": ,
        }

        list.append(new_rink)

    return list


def process_waterloo(url, locs_url, fields_url, save):
    # for working on local copy of responses
    # res_text = open("local_responses/water.html", "r", encoding="utf-8").read()
    # loc_res_text = open(
    #    "local_responses/wat_parks_locs.html", "r", encoding="utf-8"
    # ).read()

    res_text = waterloo_workaround_get_request(url)
    loc_res_text = waterloo_workaround_get_request(locs_url)
    fields_res_text = waterloo_workaround_get_request(fields_url)

    if save == True:
        save_local_response("waterloo_schedule", res_text)
        save_local_response("waterloo_parks_locs", loc_res_text)
        save_local_response("waterloo_fields_locs", fields_res_text)

    soup = BeautifulSoup(res_text, "html.parser")
    loc_soup = BeautifulSoup(loc_res_text, "html.parser")
    fields_soup = BeautifulSoup(fields_res_text, "html.parser")

    list_items = generate_waterloo_list(
        soup, loc_soup, fields_soup, get_num_rinks(soup)
    )

    return list_items
