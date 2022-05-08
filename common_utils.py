import requests
import json
import os

from datetime import datetime
from sys import platform


def platform_indep_delete(dir):
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("rm -rf {}/*".format(dir))
    elif platform == "win32":
        os.system('del /f /Q "{}\/"'.format(dir))


def save_scraped_data(filename, data):
    now = datetime.now()
    dateOut = now.strftime("%Y-%m-%d_%H%M%S")
    path_str = "scraped_data/{}_{}.json".format(dateOut, filename)

    with open(path_str , "w") as outfile:
        outfile.write(data)
        print("Saved file '{}'.".format(path_str))


def save_local_response(filename, response):
    now = datetime.now()
    dateOut = now.strftime("%Y-%m-%d_%H%M%S")
    path_str = "local_responses/{}_{}.html".format(dateOut, filename)

    with open(path_str, "w", encoding="utf-8") as f:
        f.write(response)
        print("Saved file '{}'.".format(path_str))


def jsonify_city(list_items):
    myObj = {"rinks": []}

    myObj["rinks"] = list_items

    serial = json.dumps(myObj, indent=3)
    return serial


def send_get_request(url):

    response = requests.get(url)
    code = response.status_code

    if code != 200:
        print(
            "The resource '{}' returned a non OK status code: '{}'.".format(url, code)
        )
        return code
    else:
        return response.text
