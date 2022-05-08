"""
    icy-scraper

    This program is a web scraper that automates the process of gathering information on 
    the outdoor ice skating rinks from the three largest municipalities of the Waterloo
    region. 

"""

import argparse

from datetime import datetime
from kitchener_utils import process_kitchener
from waterloo_utils import process_waterloo
from cambridge_utils import process_cambridge
from common_utils import jsonify_city, save_scraped_data


def init_parser():
    mpar = argparse.ArgumentParser(
        description="icy-scraper is a web scraper that automates the process of gathering information on the outdoor ice skating rinks from the three largest municipalities of the Waterloo region. "
    )

    mpar.add_argument(
        "City",
        metavar="city",
        type=str,
        help="Name of city to scrape. 'all' for the whole region.",
    )

    mpar.add_argument(
        "-c",
        "--count",
        action="store_true",
        help="Will include count in output if flag is present.",
    )

    mpar.add_argument(
        "-f",
        "--file",
        action="store_true",
        help="Print JSON scraper results to file.",
    )

    mpar.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="Save a local copy of the response(s).",
    )

    args = mpar.parse_args()
    args.City = args.City.lower()

    return args


def main():
    # fmt: off
    url_w_rinks_sched = "https://www.waterloo.ca/en/things-to-do/arenas-and-outdoor-rinks.aspx"
    url_w_parks_loc = "https://www.waterloo.ca/en/things-to-do/parks-directory.aspx#Parks-with-amenities"
    url_w_fields_loc = "https://www.waterloo.ca/en/things-to-do/sport-fields-and-courts.aspx"
    url_c = "https://facilities.cambridge.ca/?CategoryIds=82&FacilityTypeIds="
    url_k = "https://www.kitchener.ca/en/recreation-and-sports/outdoor-skating-rinks.aspx"

    args = init_parser()

    results = []

    match args.City:
        case "kitchener":
            results = process_kitchener(url_k, args.save)
            
            jsonifyCityResults = jsonify_city(results)

            if args.save == False and args.file == False:
                print(jsonifyCityResults)

            if args.file == True:
                save_scraped_data("kitchener", jsonifyCityResults)

            if args.count == True:
                print("{} results returned.".format(len(results)))

        case "cambridge":
            results = process_cambridge(url_c, args.save)
            
            jsonifyCityResults = jsonify_city(results)

            if args.save == False and args.file == False:
                print(jsonifyCityResults)

            if args.file == True:
                save_scraped_data("cambridge", jsonifyCityResults)

            if args.count == True:
                print("{} results returned.".format(len(results)))

        case "waterloo":
            results = process_waterloo(url_w_rinks_sched, url_w_parks_loc, url_w_fields_loc, args.save)

            jsonifyCityResults = jsonify_city(results)

            if args.save == False and args.file == False:
                print(jsonifyCityResults)

            if args.file == True:
                save_scraped_data("waterloo", jsonifyCityResults)
            
            if args.count == True:
                print("{} results returned.".format(len(results)))

        case "all":
            results = process_waterloo(url_w_rinks_sched, url_w_parks_loc, url_w_fields_loc, args.save)
            results += process_cambridge(url_c, args.save)
            results += process_kitchener(url_k, args.save)

            jsonifyCityResults = jsonify_city(results)

            if args.save == False and args.file == False:
                print(jsonifyCityResults)

            if args.file == True:
                save_scraped_data("all", jsonifyCityResults)
   
            if args.count == True:
                print("{} results returned.".format(len(results)))

    # fmt: on


if __name__ == "__main__":
    main()
