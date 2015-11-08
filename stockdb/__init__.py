#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stocks.db")

def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create table
    c.execute("""CREATE TABLE stocks (
    symbol INTEGER,
    date TEXT,
    company_name TEXT,
    max_price REAL,
    min_price REAL,
    start_price REAL,
    end_price REAL,
    PRIMARY KEY (symbol, date)
    )""")
    conn.commit()
    c.close()

def insert_db(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if any(isinstance(i, list) for i in data):
        # if data is a nested list (means multiple data)
        c.executemany("INSERT INTO stocks VALUES (?,?,?,?,?,?,?)",  data)
    else:
        # assuming that data is just one row
        c.execute("INSERT INTO stocks VALUES (?,?,?,?,?,?,?)", data)
    conn.commit()
    c.close()

if __name__ == "__main__":
    create_db()
