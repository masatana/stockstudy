#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3

import pandas

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
    volume INT,
    traiding_value INT,
    PRIMARY KEY (symbol, date)
    )""")
    conn.commit()
    c.close()

if __name__ == "__main__":
    create_db()
