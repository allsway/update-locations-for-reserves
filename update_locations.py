#!/usr/bin/python
import requests
import sys
import csv
import ConfigParser
import xml.etree.ElementTree as ET

def createurl(row):
	bib_id = row[0]
	holding_id = row[1]
	item_id = row[2]
	return '/almaws/v1/bibs/' + bib_id + '/holdings/'+ holding_id +'/items/' + item_id; 
	

# Read campus parameters
config = ConfigParser.RawConfigParser()
config.read(sys.argv[1])
apikey = config.get('Params', 'apikey')
baseurl = config.get('Params','baseurl')
campuscode =  config.get('Params', 'campuscode')
headers = {"Content-Type": "application/xml"}

# CSV file of former location codes to Alma location codes
location_map = sys.argv[2]





"""f = open(items_file, 'rt')
try:
    reader = csv.reader(f)
    reader.next() #skip header line
    for row in reader:
    	if row[0] != 'end-of-file':
			apicall = createurl(row)
			url =  baseurl + apicall + '?apikey=' + apikey
			print url
			response = requests.get(url)
			
			item = ET.fromstring(response.content)
			for item_data in item.findall("item_data"):
				item_data.find('library').text = library
				item_data.find('location').text = location
#				item_data.find('location').set('desc',location_desc)
			print ET.tostring(item)
			r = requests.put(url,data=ET.tostring(item),headers=headers)
			print r.content

finally:
    f.close()"""
	







