#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from functools import partial
from datetime import datetime
import sqlite3
import os
import urllib.request
import time
import datetime
import csv
import argparse
import sys


import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker

STOCK_URL = "http://k-db.com/stocks/{code}-T?year={year}&download=csv"
NIKKEI_URL = "http://k-db.com/indices/I101?year={year}&download=csv"

def format_date(x, pos=None, N=None, r=None):
    thisind = np.clip(int(x+0.5), 0, N-1)
    return r.date[thisind].strftime("%Y-%m-%d")

def format_response(response):
    return "\n".join(
            response
            .read()
            .decode(encoding="Shift-JIS")
            .replace("\r\n", "\n")
            .strip()
            .split()[2:])

def crawl(ticker_symbols):
    if not os.path.isdir("./csv"):
        os.makedirs("./csv")    
    for code, name in ticker_symbols.items():
        with open("./csv/{code}.csv".format(code=code), "w") as f:
            for year in range(2007, datetime.today().year+1):
                response = urllib.request.urlopen(STOCK_URL.format(code=code, year=year))
                formatted_response = format_response(response)
                if format_response.endswith("\n"):
                    f.write(formatted_response)
                else:
                    f.write(formatted_response+"\n")
            time.sleep(1)

    # NIKKEI STOCK AVERAGE
    with open("./csv/NIKKEI.csv", "w") as f:
        for year in range(2007, datetime.today().year+1):
            response = urllib.request.urlopen(NIKKEI_URL.format(code=code, year=year))
            formatted_response = format_response(response)
            if format_response.endswith("\n"):
                f.write(formatted_response)
            else:
                f.write(formatted_response+"\n")
        time.sleep(1)

def analyze(ticker_symbols):
    col_names = (
        "date",
        "start_price",
        "max_price",
        "min_price",
        "end_price",
        "volume",
        "trading_value",
    )
    for code in ticker_symbols:
        print(code)
        dat = mlab.csv2rec("./csv/{code}.csv".format(code=code),
                skiprows=2, names=col_names)
        N = len(dat)
        ind = np.arange(N)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(ind, dat.end_price)
        applied_format_date = partial(format_date, N=N, r=dat)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(applied_format_date))
        fig.autofmt_xdate()
        plt.savefig("./image_{code}.png".format(code=code))

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stocks.db")

def create_db(symbols):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE symbols (
    symbol INT,
    company_name TEXT,
    PRIMARY KEY (symbol)
    )""")
    conn.commit()
    for symbol, company_name in symbols.items():
        c.execute("INSERT INTO symbols VALUES (?, ?)", (symbol, company_name))
        conn.commit()

    for symbol in symbols:
        c.execute("""CREATE TABLE {symbol} (
        date TEXT,
        start_price REAL,
        max_price REAL,
        min_price REAL,
        end_price REAL,
        volume INT,
        trading_value INT,
        PRIMARY KEY (date)
        )""".format(symbol=symbol))
        conn.commit()
    c.close()


def store(symbols):
    col_names = (
        "date",
        "start_price",
        "max_price",
        "min_price",
        "end_price",
        "volume",
        "trading_value",
    )
    if os.path.isfile(DB_PATH):
        create_db()
    con = sqlite3.connect(DB_PATH)
    for symbol in symbols:
        df = pandas.read_csv("./csv/{symbol}.csv".format(symbol=symbol),
                names=col_names)
        df.to_sql(symbol, con=con, if_exists="append")

if __name__ == "__main__":
    with open("./symbols.list") as f:
        symbols = {int(codename.strip().split()[0]) : codename.strip().split()[1]
                for codename in f}
    if sys.argv[0] == "crawl":
        crawl(symbols)
    elif sys.argv[0] == "store":
        store(symbols)
    elif sys.argv[0] == "analyze":
        analyze(symbols)
    else:
        print("Type: (crawl|store|analyze)")
