import urllib2
import time
import math
import numpy as np

#fetch building info with the api
url = 'http://berkeley.openbms.org/api/'

json = urllib2.urlopen(url).read()

(true,false,null) = (True,False,None)
profiles = eval(json)

for testbuilding in profiles:
	print testbuilding['longname']

	#assemble queryids - pre-subsampled ids are in FINALidA, apply-sum ids are in FINALidB
	if testbuilding['queryid'] == None or testbuilding['queryid'] == '':
		testbuilding['FINALidA'] = testbuilding['longname']
	else:
		testbuilding['FINALidA'] = testbuilding['queryid']

	if testbuilding['sumQueryid'] == None or testbuilding['sumQueryid'] == '':
		testbuilding['FINALidB'] = testbuilding['FINALidA']
	else:
		testbuilding['FINALidB'] = testbuilding['sumQueryid']

	print testbuilding['FINALidA']
	print testbuilding['FINALidB']


	#start subsample/baseline querying
	firsturl = 'http://berkeley.openbms.org/ARDgetData/api/query?'
	tagQ = "select * where Metadata/Location/Building = '" + testbuilding['FINALidA'] + "' and (Metadata/Extra/Operator like 'baseline-%' or (Metadata/Extra/Operator = 'subsampled sum')) and not (Metadata/Path like '1-hr') and not (Metadata/Extra/Resample like 'subsample-mean-3600') and not (Metadata/Extra/Type like 'steam baseline')"

	result = eval(urllib2.urlopen(firsturl, tagQ).read())
	print result

	currenttime = int((time.time())) * 1000
	starttime = currenttime - 24*60*60000

	for x in range(len(result)):
		secondurl = "http://berkeley.openbms.org/ARDgetData/api/data/uuid/" + result[x]['uuid'] + "?starttime=" + str(starttime) + "&endtime=" + str(currenttime)

		result2 = eval(urllib2.urlopen(secondurl).read())
		result2 = np.array(result2[0]['Readings']) #now the baseline data is stored as a numpy array
		print result2



#counter = 0
#for x in profiles:
#	counter += 1
#	print x['longname'] + " " + 

#print counter
