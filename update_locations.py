#!/usr/bin/python
import requests
import sys
import csv
import ConfigParser
import logging
import xml.etree.ElementTree as ET


def get_key():
	return config.get('Params', 'apikey')
	
def get_campus_code():
	return config.get('Params', 'campuscode')
	
def get_sru_base():
	return config.get('Params', 'sru')
	
def get_base_url():
	return config.get('Params', 'baseurl')

def get_location_mapping():
	return config.get('Params', 'locations')
	


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
	Read in item csv file of items exported from Millennium/Sierra that contain a SAVE ITEM field
"""
def read_items(item_file):
	f  = open(item_file,'rt')
	try:
		reader = csv.reader(f)
		header = reader.next()
		locations = read_location_mapping(get_location_mapping())
		for row in reader:
			print row
			parse_row(row,locations)

	finally:
		f.close()


"""
	Makes PUT request for item with updated location and temporary location information	
"""	
def post_item(item,barcode):
	item_url =  item.attrib['link'] + "?apikey=" +  get_key()
	headers = {"Content-Type": "application/xml"}
	r = requests.put(item_url,data=ET.tostring(item),headers=headers)
	print r.content

	
"""
	Returns the item's permanent location from the SAVE ITEM field
"""	
def get_permanent_location(save_item_info):
	olocat = save_item_info.split(',')[1]
	loc = olocat.split('=')[1]
	return loc.strip()

"""
	Parse item data
"""
def parse_row(row,locations):
	barcode = row[0]
	save_item_info = row[2]
	permanent_location = get_permanent_location(save_item_info)
	item = get_item_xml(barcode)
	if item is not None:
		if item.find("holding_data/in_temp_location").text != 'true':
			temp_location = item.find("item_data/location").text
			temp_library = item.find("item_data/library").text
			temp_location_desc = item.find("item_data/location").attrib['desc']
			temp_library_desc = item.find("item_data/library").attrib['desc']
			new_temp_library = item.find("holding_data/temp_library")
			new_temp_location = item.find("holding_data/temp_location")
			in_temp_location = item.find("holding_data/in_temp_location")
			in_temp_location.text =  "true"
			new_temp_location.text = temp_location
			new_temp_library.text = temp_library
			perm_location = item.find("item_data/location")
			perm_library = item.find("item_data/library")
			perm_location.text = locations[permanent_location]['location']
			perm_library.text = locations[permanent_location]['library']
			print ET.tostring(item)
			post_item(item,barcode)
		else:
			logging.info("Item already in temporary location: " + barcode)


"""
	Get item info based on item barcode
"""
def get_item_xml(barcode):
	item_url = get_base_url() + "/items?item_barcode=" + barcode +  "&apikey=" + get_key()
	response = requests.get(item_url)
	if response.status_code != 200:
		logging.info("Item not found for item barcode: " + barcode)
		return None
	print ET.fromstring(response.content)
	item = ET.fromstring(response.content)
	return item


config = ConfigParser.RawConfigParser()
config.read(sys.argv[1])
logging.basicConfig(filename='status.log',level=logging.DEBUG)
items_file = sys.argv[2]
read_items(items_file)



















