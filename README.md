# update-locations-for-reserves
For all items in the provided file, moves the item's current permanent location to the item's temporary location, and updates item's permanent location to location stored in the former SAVE ITEM location field in Millennium/Sierra,

####Steps for extracting data from Millennium/Sierra
In Create Lists, create a list of ITEMS where the 7 SAVE ITEM field 'exists'
Export this list of records and select the following fields to export 
* BARCODE  
* 7 SAVE ITEM

####config.txt
A configuration file that stores your API key, base API URL and yout location mapping file. 
```
[Params]
apikey: apikey 
baseurl: host
locationmap: path_to_data_inputs/location.csv
```

####update-items.py
Takes as arguments:
- the configuration file with the settings listed above
- a csv file of item barcodes and the corresponding item SAVE ITEM field, the following format:

```  
"barcode","Save item"
"30050017268193","OITYPE=40, OLOCAT=jff  , OCHKOUT=1"
```

Run as `python ./update-items.py {config.txt} {item_data.csv}`
