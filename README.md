# update-locations-for-reserves
For all items in the provided file, moves the item's current permanent location to the item's temporary location, and updates item's permanent location to location stored in the former SAVE ITEM location field in Millennium/Sierra,

####Steps for extracting data from Millennium/Sierra
In Create Lists, create a list of ITEMS where the 7 SAVE ITEM field 'exists'
Export this list of records and select the following fields to export 
* BARCODE  
* 7 SAVE ITEM

This file is your {item_data.csv} file

####get_save_items.sql
For Sierra campuses, this query can be used instead of Create Lists to extract the item BARCODE and SAVE ITEM fields. 

####config.txt
A configuration file that stores your API key, base API URL and yout location mapping file. The base API URL is in the following format: https://api-na.hosted.exlibrisgroup.com/almaws/v1.  
```
[Params]
apikey: apikey 
baseurl: host
locationmap: path_to_data_inputs/location.csv
```
####locations.csv
Your Migration form Locations tab saved in .csv format (copy and paste the Excel Locations tab into a new Excel spreadsheet and save as a csv file to create this data input. 

####update-items.py
Takes as arguments:
- the configuration file with the settings listed above
- a csv file of item barcodes and the corresponding item SAVE ITEM field, the following format:

```  
"barcode","Save item"
"30050017268193","OITYPE=40, OLOCAT=jff  , OCHKOUT=1"
```

Run as `python ./update-items.py {config.txt} {item_data.csv}`
