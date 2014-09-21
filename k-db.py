#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
import urllib.request
import time
import datetime
import csv

import numpy as np
import matplotlib.pyplot as plt

STOCK_URL = "http://k-db.com/stocks/{code}-T?year={year}&download=csv"
NIKKEI_URL = "http://k-db.com/indices/I101?year={year}&download=csv"

def crawl(ticker_symbols):
    for code, name in ticker_symbols.items():
        for year in range(2007, 2014):
            with open("./csv/{year}_{name}.csv".format(year = year, name = name), "w") as f:
                response = urllib.request.urlopen(STOCK_URL.format(code = code, year = year))
                f.write(response.read().decode(encoding="Shift-JIS").replace("\r\n", "\n"))
            time.sleep(1)

    # NIKKEI STOCK AVERAGE
    for year in range(2007, 2014):
        with open("./csv/{year}_NIKKEI.csv".format(year = year), "w") as f:
            response = urllib.request.urlopen(NIKKEI_URL.format(code = code, year = year))
            f.write(response.read().decode(encoding="Shift-JIS").replace("\r\n", "\n"))
        time.sleep(1)

def analyze(ticker_symbols):
    data = {}
    for code, name in ticker_symbols.items():
        data[code] = {}
        for year in range(2007, 2014):
            data[code][year] = []
            with open("./csv/{year}_{name}.csv".format(year=year, name=name)) as f:
                reader = csv.reader(f)
                next(reader)
                next(reader)
                for row in reader:
                    data[code][year].append(row)

    data["NIKKEI"] = {}
    for year in range(2007, 2014):
        data["NIKKEI"][year] = []
        with open("./csv/{year}_NIKKEI.csv".format(year=year, name=name)) as f:
            reader = csv.reader(f)
            next(reader)
            next(reader)
            for row in reader:
                data["NIKKEI"][year].append(row)

    for code, year_data in data.items():
        X = []
        Y = []
        for year, rows in year_data.items():
            for row in rows:
                X.append(datetime.datetime.strptime(row[0], "%Y-%m-%d"))
                Y.append(float(row[3]))
        fig = plt.figure()
        fig.autofmt_xdate()
        Y = np.array(Y)
        plt.plot(X, Y)
        plt.savefig("./images_{code}.png".format(code=code))


if __name__ == "__main__":
    with open("./ticker_symbol.list") as f:
        ticker_symbols = {int(codename.strip().split()[0]) : codename.strip().split()[1] for codename in f}
    #crawl(ticker_symbols)
    analyze(ticker_symbols)
