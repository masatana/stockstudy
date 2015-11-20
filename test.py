#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(description="Process with k-db")
parser.add_argument("crawl", action="store_const", type=int, const=10000)
parser.add_argument("store", action="store_true")
parser.add_argument("initdb", action="store_true")
parser.parse_args()

if parser.crawl is not None:
    print("year")
