#!/usr/bin/env python

"""
NAME:

    Very simple converter from ADIF to EDI/REG1TEST format

DESCRIPTION:

    Provide ADIF format as STDIN to this script or give a filename as argv[1].
    If the ADIF input is correct, it will produce a minimalistic EDI log file
    with calculated QRB (claimed points)

TODO:
    - Check for new WWL's during the log generation
    - Support RTTY/FT8 modes
    - Multiply claimed points by band multiplier

EXAMPLES:

    adi2edi.py < logfile.adif > logfile.edi

REFERENCES:

    https://www.ok2kkw.com/ediformat.htm

"""
from datetime import date
from typing import List
import maidenhead as mh
import geopy.distance
import adif_io
import time
import sys
import os
import select

my_callsign = "LY1BWB"
my_gridsquare = "KO24PR"
my_contest = "432 MHz"


def print_reg1test_header(tdate, qsorecords):
    print("[REG1TEST;1]")
    print("TDate={};{}".format(tdate, tdate))
    print("PCall={}".format(my_callsign))
    print("PWWLo={}".format(my_gridsquare))
    print("PBand={}".format(my_contest))
    print("[QSORecords;{}]".format(qsorecords))


def get_distance(home, dxcc):
    home_loc = mh.to_location(home)
    dx_loc = mh.to_location(dxcc)
    return int(geopy.distance.geodesic(home_loc, dx_loc).km)


def print_reg1test_qsos(qsos):
    for q in qsos:
        if q["MODE"] == "CW":
            qso_mode = "2"
        if q["MODE"] == "FM" or q["MODE"] == "SSB":
            qso_mode = "6"
        if "GRIDSQUARE" in q.keys():
            qso_grid = q["GRIDSQUARE"].upper()
        elif "COMMENT" in q.keys():
            qso_grid = q["COMMENT"].upper()

        new_square = ""
        qrb = get_distance(my_gridsquare, qso_grid)
        qso_time = q["TIME_ON"][:4]
        print(
            "{};{};{};{};{};;{};;;{};{};;{};;".format(
                q["QSO_DATE"][2:],
                qso_time,
                q["CALL"],
                qso_mode,
                q["RST_SENT"],
                q["RST_RCVD"],
                qso_grid,
                qrb,
                new_square,
            )
        )


def get_adif_data():
    if not sys.stdin.isatty():
        return sys.stdin.read()
    else:
        if len(sys.argv) > 1:
            adif_filename = sys.argv[1]
            if os.path.isfile(adif_filename):
                adif_file = open(adif_filename, "r")
                _d = adif_file.read()
                adif_file.close()
                return _d
            else:
                print("Unable to open {}".format(adif_filename), file=sys.stderr)
                os._exit(2)
        else:
            print("Usage: adi2edi <file>", file=sys.stderr)
            os._exit(1)


def main():
    try:
        adif_data = get_adif_data()
    except:
        print("Error retrieving ADIF data", file=sys.stderr)
        os._exit(3)

    try:
        qsos, _header = adif_io.read_from_string(adif_data)
        print_reg1test_header(qsos[0]["QSO_DATE"], len(qsos))
    except:
        print("Unable to parse ADIF input", file=sys.stderr)
        os._exit(4)

    try:
        print_reg1test_qsos(qsos)
    except:
        print("Unable to build QSO list", file=sys.stderr)
        os._exit(5)


if __name__ == "__main__":
    main()
