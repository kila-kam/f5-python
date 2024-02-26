import json
import csv

# Opening JSON file
f = open('data.json')
 
# returns JSON object as 
# a dictionary
data = json.load(f)
#print(data)
# Closing file
f.close()

f = csv.writer(open("data.csv", "w"))
f.writerow(["name", "destination", "rules", "pool", "SNAT" , "enabled"])
for x in data['items']:
     print(x)
     try:
         f.writerow([x["name"],
         x["destination"],
         x.get("pool","Not available"),
         x.get("rules","Not available"),
         x["sourceAddressTranslation"],
         x["enabled"],
         ])
     except KeyError:
          pass
