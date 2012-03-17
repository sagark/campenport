import urllib2
import time
import math
import numpy as np
import sqlite3
#change sagar to ubuntu upon deployment
conn = sqlite3.connect('/home/sagar/dev/campenportdb/messwith.db')

#fetch building info with the api
url = 'http://berkeley.openbms.org/api/'

json = urllib2.urlopen(url).read()

(true,false,null) = (True,False,None)
profiles = eval(json)

#buildings dict format:
buildings = { }

for testbuilding in profiles:
	print "fetching: " + testbuilding['longname']

	#assemble queryids - pre-subsampled ids are in FINALidA, apply-sum ids are in FINALidB
	if testbuilding['queryid'] == None or testbuilding['queryid'] == '':
		testbuilding['FINALidA'] = testbuilding['longname']
	else:
		testbuilding['FINALidA'] = testbuilding['queryid']

	if testbuilding['sumQueryid'] == None or testbuilding['sumQueryid'] == '':
		testbuilding['FINALidB'] = testbuilding['FINALidA']
	else:
		testbuilding['FINALidB'] = testbuilding['sumQueryid']

	#print testbuilding['FINALidA']
	#print testbuilding['FINALidB']


	#start subsample/baseline querying
	firsturl = 'http://berkeley.openbms.org/ARDgetData/api/query?'
	tagQ = "select * where Metadata/Location/Building = '" + testbuilding['FINALidA'] + "' and (Metadata/Extra/Operator like 'baseline-%' or (Metadata/Extra/Operator = 'subsampled sum')) and not (Metadata/Path like '1-hr') and not (Metadata/Extra/Resample like 'subsample-mean-3600') and not (Metadata/Extra/Type like 'steam baseline')"

	result = eval(urllib2.urlopen(firsturl, tagQ).read())
	#print result

	currenttime = int((time.time())) * 1000
	starttime = currenttime - 24*60*60000



##############################################if statement here to only include those with baselines

	for x in range(len(result)):
		if x == 0:
			buildings[testbuilding['longname']] = {'origtag': testbuilding['FINALidB']}
		secondurl = "http://berkeley.openbms.org/ARDgetData/api/data/uuid/" + result[x]['uuid'] + "?starttime=" + str(starttime) + "&endtime=" + str(currenttime)

		result2 = eval(urllib2.urlopen(secondurl).read())
		result2 = result2[0]['Readings'] #now the baseline data is stored as a numpy array
		buildings[testbuilding['longname']][result[x]['Metadata']['Extra']['Operator']] = result2
		#print result2
	

#print buildings
#INVARIANT: buildings only contains buildings that have a baseline, now go through and fetch data for each one that has a baseline but no data

for building in buildings.keys():
	#print buildings[building].keys()
	if 'baseline-01' not in buildings[building].keys():
		del(buildings[building])

#print "discards buildings with no baseline"
for building in buildings.keys():
	if 'subsampled sum' not in buildings[building].keys() or buildings[building]['subsampled sum']==[]:
		print "WARNING: " + building
		applySumdata = "apply sum($1, 900, .1, .1) to  data in (" + str(starttime) + ", " + str(currenttime) + ") streamlimit 10000 where Metadata/Extra/System = 'electric'  and ((Properties/UnitofMeasure = 'kW' or Properties/UnitofMeasure = 'Watts') or Properties/UnitofMeasure = 'W') and Metadata/Location/Building like '" + buildings[building]['origtag'] + "%' and not Metadata/Extra/Operator like 'sum%' and not Path like '%demand'"
		applySumURL = 'http://berkeley.openbms.org/ARDgetData/api/query?'
		result3 = eval(urllib2.urlopen(applySumURL, applySumdata).read())
		result3 = result3[0]['Readings']
		buildings[building]['subsampled sum'] = result3
		#print result3
	#print building
	#print buildings[building].keys()

#now that all data is available:

#bin data
#compute means
#trim edges
#convert to numpy array
#compute rms
#store to DB
for building in buildings.keys():
	for datatype in buildings[building].keys():
		buildings[building][datatype]

print buildings








#write to database
for building in buildings.keys():
	cursor = conn.cursor()
	cursor.execute("UPDATE buildings_building SET rmsDEV=2340 WHERE longname='" + building + "'")
	conn.commit()
	cursor.close()


#counter = 0
#for x in profiles:
#	counter += 1
#	print x['longname'] + " " + 

#print counter
