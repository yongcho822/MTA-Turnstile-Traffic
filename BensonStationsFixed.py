import csv
import sys
import dateutil.parser
from urllib2 import urlopen
from collections import defaultdict, Counter
from pprint import pprint

csv.field_size_limit(sys.maxsize)

def writethefile(url):
    with open ("Turnstile.txt", "w") as f:
        read_url = urlopen(URL).read()
        f.write(read_url)  
        
URL = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_150627.txt'
writethefile(URL)

minidict = defaultdict(list)

with open("Turnstile.txt", "r") as f, open("TurnstileSorted.csv", "w") as out:
    r = csv.reader(f)
    throwawayline = next(r)
    for row in r:
        CA,UNIT,SCP,STATION,LINENAME,DIVISION,DATE,TIME,DESC,ENTRIES,EXITS = row
        minidict[(CA, UNIT, SCP, STATION, LINENAME)].append([DIVISION,DATE,TIME,DESC,ENTRIES,EXITS])
        
    wr = csv.writer(out, delimiter = '\t')
    wr.writerows([(k,v) for k,v in mydict.items()])

newdict = dict(minidict)

shortdict = {k : map(lambda x: [x[1], x[2], x[4]], v) for k, v in newdict.items()}

def dateconverter(a,b):
    newstring = " ".join((a,b))
    return dateutil.parser.parse(newstring)

dateconverted_dict = {k : map(lambda x: [dateconverter(x[0], x[1]), x[2]], v) for k, v in shortdict.items()}

testdict = defaultdict(list)

for key1 in dateconverted_dict:  
    numb_entries_for_wk = len(dateconverted_dict[key1])
    for i, rowvalues in enumerate(dateconverted_dict[key1]):
        #print i, rowvalues
        if i == 0:
            odometer = int(rowvalues[1])
            testdict[key1].append([rowvalues[0], 0])

        elif 0 < i < numb_entries_for_wk:
            diff = int(rowvalues[1]) - odometer
            odometer = int(rowvalues[1])
            testdict[key1].append([rowvalues[0], diff])
        
from collections import Counter
from itertools import groupby

dict_by_days = defaultdict()
interimdict = defaultdict(list)
newdict = defaultdict(int)

outlier_dict = {turnstile: [(time, count)
                            for (time, count) in rows
                            if 0 <= count <= 5000] for turnstile, rows in testdict.items()}
"""---- outlier_dict has all the outliers dropped. ----"""

for key3 in outlier_dict:
    for rowvalues in outlier_dict[key3]:
        newdates = rowvalues[0].replace(hour=0, minute=0, second=0)
        interimdict[key3].append([newdates, rowvalues[1]])

"""---- interimdict has dates all uniformed with hours.mins.secs dropped. ----"""


for fatkey in interimdict:
    eachvalblock = interimdict[fatkey]
    x = groupby(eachvalblock, lambda x1:x1[0])
    newt = []
    for y, z in x:
        ex_list = []
        for a in z:
            ex_list.append(a[1])
        #print '\n'
        newt.append([y,sum(ex_list)])
    dict_by_days[fatkey] = newt

short_data = defaultdict(Counter)

for key, value in dict_by_days.items():
    short_key = (key[3], key[4])
    short_data[short_key] += Counter(dict(dict_by_days[key]))
#--- values are Counter objects at this point
   
station_dict = dict(short_data)
for key, value in station_dict.items():
    station_dict[key] = list(list(x) for x in value.items())
for i in station_dict:
    station_dict[i].sort()

def station_totaler(station):
    total = 0 
    for i in (station_dict[station]):
        total += i[1]
    return total

station_tot_dict = {}
for key in station_dict:
    station_tot_dict[key] = station_totaler(key)

station_tot_dict_sorted = sorted(station_tot_dict.items(), key = lambda x :x[1], reverse = True)
pprint(station_tot_dict_sorted)

with open("Station_Totals.csv", "w") as out:
    writer = csv.writer(out, delimiter = ',')
    writer.writerows([(k,v) for k,v in station_tot_dict.items()])
    print 'Done here.'