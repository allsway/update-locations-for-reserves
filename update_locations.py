#!/usr/bin/python
import requests
import sys
import csv
import configparser
import logging
import re
import xml.etree.ElementTree as ET

# Returns the API key
def get_key():
    return config.get('Params', 'apikey')

# Returns the Alma API base URL
def get_base_url():
    return config.get('Params', 'baseurl')

# Returns the location mapping file, taken from the Alma Migration Form
def get_location_mapping():
    return config.get('Params', 'locations')

"""
    Read in location_map.csv and create a map between former locations and Alma locations
    [Mil/Sierra location code] => [Alma loc code, Alma Library, Alma call number type for loc]
"""
def read_location_mapping(loc_map_file):
    location_mapping = {}
    f = open(loc_map_file, 'rt')
    try:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            iiiloc = re.sub('/','',row[0].strip())
            location_mapping[iiiloc] = {'location': row[3].strip(),'library': row[2].strip()}
        return location_mapping
    finally:
        f.close()


# Read in item csv file of items exported from Millennium/Sierra that contain a SAVE ITEM field
def read_items(item_file):
    f  = open(item_file,'rt')
    try:
        reader = csv.reader(f)
        header = next(reader)
        locations = read_location_mapping(get_location_mapping())
        for row in reader:
            print (row)
            parse_row(row,locations)
    finally:
        f.close()

#    Makes PUT request for item with updated location and temporary location information
def post_item(item,barcode):
    item_url =  item.attrib['link'] + "?apikey=" +  get_key()
    headers = {"Content-Type": "application/xml"}
    r = requests.put(item_url,data=ET.tostring(item),headers=headers)
    print (r.content)

#    Returns the item's permanent location from the SAVE ITEM field
def get_permanent_location(save_item_info):
    olocat = save_item_info.split(',')[1]
    loc = olocat.split('=')[1]
    loc = re.sub('/', '', loc) # strip '/' from location codes
    print (loc)
    return loc.strip()


#    Get item XML from the Alma API, based on item barcode
def get_item_xml(barcode):
    item_url = get_base_url() + "/items?item_barcode=" + barcode +  "&apikey=" + get_key()
    print(item_url)
    response = requests.get(item_url)
    if response.status_code != 200:
        logging.info("Item not found for item barcode: " + barcode)
        return None
    print (ET.fromstring(response.content))
    item = ET.fromstring(response.content)
    return item

"""
    Perform location swap, adding temporary location based on current permanent location and updating permanent location based on the save item csv file location.
"""
def parse_row(row,locations):
    barcode = row[0]
    save_item_info = row[1]
    permanent_location = get_permanent_location(save_item_info)
    # Check if olocat code actually exists in the location mapping file
    if permanent_location in locations:
        print (permanent_location)
        item = get_item_xml(barcode)
        print (item)
        if item is not None and permanent_location != '':
            if item.find("holding_data/in_temp_location").text != 'true':
                temp_location = item.find("item_data/location").text
                if temp_location != locations[permanent_location]['location']:
                    temp_library = item.find("item_data/library").text
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
                    post_item(item,barcode)
                else:
                    logging.info("Temporary location same as permanent location: " + barcode)
            else:
                logging.info("Item already in temporary location: " + barcode)

# Read in configuration file
config = configparser.ConfigParser()
config.read(sys.argv[1])
logging.basicConfig(filename='status.log',level=logging.DEBUG)

# Read in items file, and call read_items
items_file = sys.argv[2]
read_items(items_file)
