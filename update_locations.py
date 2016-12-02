#!/usr/bin/python
import requests
import sys
import csv
import ConfigParser
import xml.etree.ElementTree as ET


def get_key():
	return config.get('Params', 'apikey')
	
def get_campus_code():
	return config.get('Params', 'campuscode')
	
def get_sru_base():
	return config.get('Params', 'sru')
	
def get_base_url():
	return config.get('Params', 'baseurl')
	


"""
	Read in location_map.csv and create map between former locations and Alma locations
	Mil/Sierra location => [Alma loc code, Alma Library, Alma call number type for loc]

"""
def read_location_mapping(loc_map_file):
	location_mapping = {}
	f = open(loc_map_file, 'rt')
	try:
		reader = csv.reader(f)
		reader.next()
		for row in reader:
			location_mapping[row[0].strip()] = {'location': row[3].strip(),'library': row[2].strip(), 'callnum' : row[4].strip()}
		return location_mapping
	finally:
		f.close()


"""
	Read in item csv file (all items in Alma)?
"""


"""
	Read in save item csv mapping based on item barcode
"""

"""
	Search SRU for item barcode, return matching bib MMS ID 
"""

"""
	Get item info based on item barcode
"""
def get_item_xml(barcode):
	item_url = get_base_url() + "/items?item_barcode=" + barcode +  "&apikey=" + get_key()
	print item_url


get_item_xml()



















