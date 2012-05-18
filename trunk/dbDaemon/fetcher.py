import urllib2
import time
import math
import numpy as np
import sqlite3
import copy
#change sagar to ubuntu upon deployment
conn = sqlite3.connect('/home/sagar/dev/campenportdb/buildinginfo.db')

#fetch building info with the api
url = 'http://berkeley.openbms.org/api/'

json = urllib2.urlopen(url).read()

(true,false,null) = (True,False,None)
profiles = eval(json)

#buildings dict format:
buildings = { }

for testbuilding in profiles:
	#if testbuilding['longname'] != 'Soda Hall':
	#	continue
	print "baseline fetch: " + testbuilding['longname']

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
	tagQ = "select * where Metadata/Location/Building = '" + testbuilding['FINALidA'] + "' and (Metadata/Extra/Operator like 'baseline-%') and not (Metadata/Extra/Operator like 'subsampled sum') and not (Metadata/Path like '1-hr') and not (Metadata/Extra/Resample like 'subsample-mean-3600') and not (Metadata/Extra/Type like 'steam baseline')"

	result = eval(urllib2.urlopen(firsturl, tagQ).read())
	#print result

	currenttime = int((time.time())) * 1000
	starttime = currenttime - 24*60*60000



##############################################if statement here to only include those with baselines
	buildings[testbuilding['longname']] = {'origtag': testbuilding['FINALidB']}

	for x in range(len(result)):
		#if x == 0:
		secondurl = "http://berkeley.openbms.org/ARDgetData/api/data/uuid/" + result[x]['uuid'] + "?starttime=" + str(starttime) + "&endtime=" + str(currenttime)

		result2 = eval(urllib2.urlopen(secondurl).read())
		result2 = result2[0]['Readings'] #now the baseline data is stored as a numpy array
		buildings[testbuilding['longname']][result[x]['Metadata']['Extra']['Operator']] = result2
		#print result2

print(buildings.keys())
for building in buildings.keys():
	# fetches actual data for all buildings (used later in all_buildings)
	if 'subsampled sum' not in buildings[building].keys() or buildings[building]['subsampled sum']==[]:
		print "actual fetch: " + building
		applySumdata = "apply nansum(axis=1) < paste < window(first, field='minute', increment=1) < units to  data in (" + str(starttime) + ", " + str(currenttime) + ") streamlimit 10000 where Metadata/Extra/System = 'electric'  and ((Properties/UnitofMeasure = 'kW' or Properties/UnitofMeasure = 'Watts') or Properties/UnitofMeasure = 'W') and Metadata/Location/Building like '" + buildings[building]['origtag'] + "%' and not Metadata/Extra/Operator like 'sum%' and not Path like '%demand' and not Path like '%demand' and not Path like '/Cory_Hall/Electric_5A7/ABC/real_power' and not Path like '/Cory_Hall/Electric_5B7/ABC/real_power'"
		applySumURL = 'http://berkeley.openbms.org/ARDgetData/api/query?'
		result3 = eval(urllib2.urlopen(applySumURL, applySumdata).read())
		result3 = result3[0]['Readings']
		buildings[building]['subsampled sum'] = result3

all_buildings = copy.deepcopy(buildings)
#performs operations for all buildings
for building in all_buildings.keys():
	print("current building is: " + str(building))
	try:
		temp = np.array(all_buildings[building]['subsampled sum'])
		actual_mean = np.mean(temp[0:,1])
		actual_max = np.amax(temp[0:,1])
		all_buildings[building]['peak_avg'] = int(actual_max/actual_mean*100)/100.0
	except:
		all_buildings[building]['peak_avg'] = 0.0
		print(all_buildings[building]['subsampled sum'])
		#asdf = raw_input("Press Enter to continue...")
	print("peak to avg: " + str(all_buildings[building]['peak_avg']))
#

buildings2 = {}

for building in buildings.keys():
	if 'baseline-01' in buildings[building].keys():
		buildings2[building] = buildings[building]

buildings = {}
buildings = buildings2


#####################################################
for building in buildings.keys():
	# this removes buildings without a baseline the buildings dict
	if 'baseline-01' not in buildings[building].keys():
		#del(buildings[building])
		pass
	else:
		try:
			temp = np.array(buildings[building]['baseline-01'])
			buildings[building]['mean'] = np.mean(temp[0:,1])
			print buildings[building]['mean']
		except:
			print 'ERR'
######################################################
# from this point on, buildings contains only buildings with a baseline and
# all_buildings contains all buildings



#now that all data is available:


def bucketize(inputdata, starttime, endtime):
	avgbucketsize = 15*60000
	averaged = []
	newendtime = endtime-endtime%avgbucketsize
	newstarttime = starttime + (avgbucketsize-starttime%avgbucketsize)
	thisUUIDoutput = []
	thisUUIDdata = inputdata
	upperbound = newendtime
	lowerbound = newendtime - avgbucketsize
	while len(thisUUIDdata) != 0:
		avgtopTracker = 0
		counter = 0
		while len(thisUUIDdata) != 0 and thisUUIDdata[len(thisUUIDdata)-1][0]>lowerbound:
			counter+=1
			avgtopTracker += thisUUIDdata.pop()[1]
		try:
			theCalcdAvg = avgtopTracker/counter
		except ZeroDivisionError:
			theCalcdAvg = None
		if (theCalcdAvg != None):
			thisUUIDoutput.append([upperbound, theCalcdAvg])
		upperbound = lowerbound
		lowerbound = upperbound - avgbucketsize
	averaged = thisUUIDoutput
	return averaged


def cleanEdges(averaged1, averaged2):
	while averaged1[0][0]<averaged2[0][0]:
		averaged2.pop(0)
	while averaged1[0][0]>averaged2[0][0]:
		averaged1.pop(0)
	while averaged1[len(averaged1)-1][0]<averaged2[len(averaged2)-1][0]:
		averaged1.pop() 
	while averaged1[len(averaged1)-1][0]>averaged2[len(averaged2)-1][0]:
		averaged2.pop()
	return[averaged1, averaged2]


#bin data
#compute means
#trim edges
#convert to numpy array
#compute rms
#store to DB
for building in buildings.keys():
	for datatype in buildings[building].keys():
		if datatype not in ['origtag', 'mean']:
			buildings[building][datatype] = bucketize(buildings[building][datatype], starttime, currenttime)
	try:
		buildings[building]['subsampled sum'], buildings[building]['baseline-01'] = cleanEdges(buildings[building]['subsampled sum'], buildings[building]['baseline-01'])
	except:
		pass


#####now compute rms, peak/avg:
for building in buildings.keys():
	actual = buildings[building]['subsampled sum']
	pred = buildings[building]['baseline-01']
	total = 0
	counter = 0
	maxSoFar = 0
	#stand_mean_numer = 0
	#stand_mean_denom = 0
	#print actual
	#print pred
	try:
		for x in range(len(actual)):
			if actual[x][1]>maxSoFar:
				maxSoFar = actual[x][1]
			#stand_mean_numer += actual[x][1]
			#stand_mean_denom += 1
			total += (actual[x][1]-pred[x][1])**2
			counter += 1
		rms = total/counter
	except ZeroDivisionError:
		rms = 0
	except:
		print("forloopissue")
		rms = 0
	
	#if stand_mean_denom != 0:
	#	stand_mean = int(stand_mean_numer/stand_mean_denom*100)/100.0
	#else:
	#	stand_mean = 0
	rms = math.sqrt(rms)
	buildings[building]['rms'] = int(rms*100)/100.0
	#buildings[building]['mean'] = stand_mean
	buildings[building]['max'] = maxSoFar
	buildings[building]['peak_avg'] = int(maxSoFar/buildings[building]['mean']*100)/100.0
	print "rms: " + str(rms)
	print "peak/avg: " + str(buildings[building]['peak_avg'])
	try:
		#temp = np.array(actual)
		#mean = np.mean(temp[0:,1])
		rmsPercentErr = int(rms/buildings[building]['mean']*10000)/100.00
		buildings[building]['rmsPercentErr'] = rmsPercentErr
		print "rms%err: " + str(rmsPercentErr)
	except:
		buildings[building]['rmsPercentErr'] = 0
	





#write to database for baselined buildings
for building in buildings.keys():
	cursor = conn.cursor()
	cursor.execute("UPDATE buildings_building SET rmsDev=" + str(buildings[building]['rms']) + " WHERE longname='" + building + "'")
	cursor.execute("UPDATE buildings_building SET rmsPercentErr=" + str(buildings[building]['rmsPercentErr']) + " WHERE longname='" + building + "'")
	conn.commit()
	cursor.close()

#write to database for all buildings
for building in all_buildings.keys():
	cursor = conn.cursor()
	print("adding to db " + building)
	cursor.execute("UPDATE buildings_building SET peak_avg=" + str(all_buildings[building]['peak_avg']) + " WHERE longname='" + building + "'")
	conn.commit()
	cursor.close()
