#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from functools import partial
import urllib.request
import time
import datetime
import csv


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker

STOCK_URL = "http://k-db.com/stocks/{code}-T?year={year}&download=csv"
NIKKEI_URL = "http://k-db.com/indices/I101?year={year}&download=csv"

def format_date(x, pos=None, N=None, r=None):
    thisind = np.clip(int(x+0.5), 0, N-1)
    return r.date[thisind].strftime("%Y-%m-%d")

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
    col_names = ("date", "initial", "high", "low", "end",)
    for code, name in ticker_symbols.items():
        for year in range(2007, 2014):
            dat = mlab.csv2rec("./csv/{year}_{name}.csv".format(year=year, name=name), skiprows=2, names=col_names)
            N = len(dat)
            ind = np.arange(N)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(ind, dat.end, "o-")
            applied_format_date = partial(format_date, N=N, r=dat)
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(applied_format_date))
            fig.autofmt_xdate()
            plt.savefig("./image_{code}_{year}.png".format(code=code, year=year))

if __name__ == "__main__":
    with open("./ticker_symbol.list") as f:
        ticker_symbols = {int(codename.strip().split()[0]) : codename.strip().split()[1] for codename in f}
    #crawl(ticker_symbols)
    analyze(ticker_symbols)
