"""
    icy-scraper-autoInsert

    This takes the output of the web scraper and adds it to the database. 

"""
import argparse
import difflib
import json
import pymssql
from prettytable import PrettyTable

dbaseAddr = "icydbserver.database.windows.net"
dbaseUser = ""
dbasePassword = ""
dbase = "icydb"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def init_parser():
    mpar = argparse.ArgumentParser(
        description="This application adds the data collected by icy-scraper to the database."
    )

    mpar.add_argument(
        "File",
        metavar="file",
        type=str,
        help="Name of the file to load",
    )

    args = mpar.parse_args()

    return args


def readVenues():
    conn = pymssql.connect(dbaseAddr, dbaseUser, dbasePassword, dbase)
    cursor = conn.cursor(as_dict=True)

    command = 'SELECT venue.venueID, venue.locationID, venue.name, venue.status, CONVERT(varchar, venue.openTime, 8) AS "openTime", CONVERT(varchar, venue.closeTime, 8) AS "closeTime", address.street, address.city, address.province, address.country, coordinate.latitude, coordinate.longitude FROM ((( venue INNER JOIN location ON venue.locationID = location.locationID) INNER JOIN address ON location.addressID = address.addressID) INNER JOIN coordinate ON location.coordinateID = coordinate.coordinateID);'
    cursor.execute(command)
    allData = cursor.fetchall()

    conn.close()

    return allData


def readFile(fileName):
    with open(fileName) as json_file:
        fileData = json.load(json_file)
        fileData = fileData["rinks"]

    return fileData


def writeNewData(data):
    conn = pymssql.connect(dbaseAddr, dbaseUser, dbasePassword, dbase)
    cursorID = conn.cursor()
    cursor = conn.cursor()

    for entry in data:
        cursorID.execute(
            "SELECT addressID, coordinateID FROM location WHERE locationID = "
            + str(entry[0])
        )
        ids = cursorID.fetchall()
        addressID = ids[0][0]
        coordinateID = ids[0][1]
        cursor.execute(
            "UPDATE venue SET status = '"
            + entry[3]
            + "', openTime = '"
            + entry[4]
            + "', closeTime = '"
            + entry[5]
            + "' WHERE locationID = "
            + str(entry[0])
        )
        cursor.execute(
            "UPDATE address SET street = '"
            + entry[2]
            + "' WHERE addressID = "
            + str(addressID)
        )
        cursor.execute(
            "UPDATE coordinate SET latitude = "
            + str(entry[6])
            + ", longitude = "
            + str(entry[7])
            + " WHERE coordinateID = "
            + str(coordinateID)
        )

    conn.commit()


def main():
    args = init_parser()

    dbaseData = readVenues()
    fileData = readFile(args.File)

    count = 0

    tableOriginal = PrettyTable(
        [
            "locationID",
            "Name",
            "Street",
            "Status",
            "openTime",
            "closeTime",
            "Latitude",
            "Longitude",
        ]
    )
    tableUpdate = PrettyTable(
        [
            "locationID",
            "Name",
            "Street",
            "Status",
            "openTime",
            "closeTime",
            "Latitude",
            "Longitude",
        ]
    )
    updateData = []

    for line in fileData:
        for row in dbaseData:
            ratio = difflib.SequenceMatcher(
                None, row["name"].replace("Rink", "").strip(), line["name"]
            ).ratio()
            if ratio > 0.85:
                tableOriginal.add_row(
                    (
                        [
                            row["locationID"],
                            row["name"],
                            row["street"],
                            row["status"],
                            row["openTime"],
                            row["closeTime"],
                            row["latitude"],
                            row["longitude"],
                        ]
                    )
                )

                if line.get("status") is None and line.get("latitude") is None:
                    if line["streetAddress"] == "Unknown":
                        tableUpdate.add_row(
                            (
                                [
                                    row["locationID"],
                                    row["name"],
                                    row["street"],
                                    row["status"],
                                    row["openTime"],
                                    row["closeTime"],
                                    row["latitude"],
                                    row["longitude"],
                                ]
                            )
                        )
                        updateData.append(
                            (
                                [
                                    row["locationID"],
                                    row["name"],
                                    row["street"],
                                    row["status"],
                                    row["openTime"],
                                    row["closeTime"],
                                    row["latitude"],
                                    row["longitude"],
                                ]
                            )
                        )
                    else:
                        tableUpdate.add_row(
                            (
                                [
                                    row["locationID"],
                                    row["name"],
                                    line["streetAddress"],
                                    row["status"],
                                    row["openTime"],
                                    row["closeTime"],
                                    row["latitude"],
                                    row["longitude"],
                                ]
                            )
                        )
                        updateData.append(
                            (
                                [
                                    row["locationID"],
                                    row["name"],
                                    line["streetAddress"],
                                    row["status"],
                                    row["openTime"],
                                    row["closeTime"],
                                    row["latitude"],
                                    row["longitude"],
                                ]
                            )
                        )
                elif line.get("status") is None and line.get("latitude") is not None:
                    if line["latitude"] == 0.0 and line["longitude"] == 0.0:
                        if line["streetAddress"] == "Unknown":
                            tableUpdate.add_row(
                                (
                                    [
                                        row["locationID"],
                                        row["name"],
                                        row["street"],
                                        row["status"],
                                        row["openTime"],
                                        row["closeTime"],
                                        row["latitude"],
                                        row["longitude"],
                                    ]
                                )
                            )
                            updateData.append(
                                (
                                    [
                                        row["locationID"],
                                        row["name"],
                                        row["street"],
                                        row["status"],
                                        row["openTime"],
                                        row["closeTime"],
                                        row["latitude"],
                                        row["longitude"],
                                    ]
                                )
                            )
                        else:
                            tableUpdate.add_row(
                                (
                                    [
                                        row["locationID"],
                                        row["name"],
                                        line["streetAddress"],
                                        row["status"],
                                        row["openTime"],
                                        row["closeTime"],
                                        row["latitude"],
                                        row["longitude"],
                                    ]
                                )
                            )
                            updateData.append(
                                (
                                    [
                                        row["locationID"],
                                        row["name"],
                                        line["streetAddress"],
                                        row["status"],
                                        row["openTime"],
                                        row["closeTime"],
                                        row["latitude"],
                                        row["longitude"],
                                    ]
                                )
                            )
                    else:
                        if line["streetAddress"] == "Unknown":
                            tableUpdate.add_row(
                                (
                                    [
                                        row["locationID"],
                                        row["name"],
                                        row["street"],
                                        row["status"],
                                        row["openTime"],
                                        row["closeTime"],
                                        line["latitude"],
                                        line["longitude"],
                                    ]
                                )
                            )
                            updateData.append(
                                (
                                    [
                                        row["locationID"],
                                        row["name"],
                                        row["street"],
                                        row["status"],
                                        row["openTime"],
                                        row["closeTime"],
                                        line["latitude"],
                                        line["longitude"],
                                    ]
                                )
                            )
                        else:
                            tableUpdate.add_row(
                                (
                                    [
                                        row["locationID"],
                                        row["name"],
                                        line["streetAddress"],
                                        row["status"],
                                        row["openTime"],
                                        row["closeTime"],
                                        line["latitude"],
                                        line["longitude"],
                                    ]
                                )
                            )
                            updateData.append(
                                (
                                    [
                                        row["locationID"],
                                        row["name"],
                                        line["streetAddress"],
                                        row["status"],
                                        row["openTime"],
                                        row["closeTime"],
                                        line["latitude"],
                                        line["longitude"],
                                    ]
                                )
                            )
                else:
                    if line["streetAddress"] == "Unknown":
                        tableUpdate.add_row(
                            (
                                [
                                    row["locationID"],
                                    row["name"],
                                    row["street"],
                                    line["status"],
                                    line["openTime"],
                                    line["closeTime"],
                                    line["latitude"],
                                    line["longitude"],
                                ]
                            )
                        )
                        updateData.append(
                            (
                                [
                                    row["locationID"],
                                    row["name"],
                                    row["street"],
                                    line["status"],
                                    line["openTime"],
                                    line["closeTime"],
                                    line["latitude"],
                                    line["longitude"],
                                ]
                            )
                        )
                    else:
                        tableUpdate.add_row(
                            (
                                [
                                    row["locationID"],
                                    row["name"],
                                    line["streetAddress"],
                                    line["status"],
                                    line["openTime"],
                                    line["closeTime"],
                                    line["latitude"],
                                    line["longitude"],
                                ]
                            )
                        )
                        updateData.append(
                            (
                                [
                                    row["locationID"],
                                    row["name"],
                                    line["streetAddress"],
                                    line["status"],
                                    line["openTime"],
                                    line["closeTime"],
                                    line["latitude"],
                                    line["longitude"],
                                ]
                            )
                        )

                count += 1

    print("These values:")
    print(tableOriginal)
    print("Will be changed to:")
    print(tableUpdate)
    print("Total entries to change: " + bcolors.UNDERLINE + str(count) + bcolors.ENDC)

    print(
        bcolors.WARNING
        + "WARNING: This operation will OVERWRITE everything in the database."
    )
    print("Continue with these changes? (y/n)" + bcolors.ENDC)
    userDecision = str(input())

    if userDecision.lower() == "y":
        print(bcolors.OKGREEN + "Writing data to database.")
        writeNewData(updateData)

    print(bcolors.OKBLUE + "All done! Good day!" + bcolors.ENDC)


if __name__ == "__main__":
    main()
