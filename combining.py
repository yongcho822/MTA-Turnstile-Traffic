
# coding: utf-8

# In[35]:

import csv
from operator import itemgetter
from pprint import pprint

combined_dict = {}
geocode_dict = {}

with open("Station_Totals.csv", "r") as total, open("nycturnstiles/geocoded.csv", "r") as geocode:
    total_read = csv.reader(total)
    geocode_read = csv.reader(geocode)
    #row_count = sum(1 for row in total_read) - making sure there are 384 stations in our total.csv file

    with open("combinedinfo.csv", "w") as combined:
        fields = ['Station', 'Total', 'Lat', 'Lng']
        writer = csv.DictWriter(combined, fieldnames = fields, delimiter = ',')
        writer.writeheader()
        
        for row in geocode_read:
            splitrow = [row.split(',') for row in row]
            lat = itemgetter(5)(splitrow)[0]
            lng = itemgetter(6)(splitrow)[0]
            station = (itemgetter(2)(splitrow)[0], itemgetter(3)(splitrow)[0])
#             station = itemgetter(2)(splitrow)[0]
            geocode_dict[station] = [lat, lng]
#             print station
#             print type(station)
        
        count = 0

        for row in total_read:
            station_name = eval(row[0])
            totals = row[1]
            if station_name in geocode_dict:
                count += 1
                combined_dict["Station"] = station_name
                combined_dict["Total"] = totals
                combined_dict["Lat"] = geocode_dict[station_name][0]
                combined_dict["Lng"] = geocode_dict[station_name][1]
                writer.writerow(combined_dict)
        #print count - 384 matches

print 'Done here.'

