#!/usr/bin/python
import csv
import sys
import re

def read_items(items):
    f = open(items, 'rt')
    try:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if re.match('i', row[1]):
                print (row[1] + "," + row[9])
            else:
                i = 0
                reached_item = False
                while i < len(row) and reached_item is not True:
                    if re.match('i', row[i]):
                        reached_item = True
                        if row[i+9] is not None:
                            # 16
                            print (row[i] + "," + row[i+4])
                    else:
                        i += 1
    finally:
        f.close()

items = sys.argv[1]
read_items(items)
