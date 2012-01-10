from django.shortcuts import render_to_response
from campenport.buildings.models import Building

def buildings(request, buildname):
	SHORT_NAME = buildname
	try:
		thisbuilding = Building.objects.get(shortname = SHORT_NAME)
	except:
		ERR_BUILD = SHORT_NAME
		return render_to_response('buildingDNE.html', locals())

	BUILDING_NAME = thisbuilding.longname #required

	UUID_0 = thisbuilding.uuid_0
	UUID_0s30 = thisbuilding.uuid_0_sub30
	UUID_0s36 = thisbuilding.uuid_0_sub36
	UUID_1 = thisbuilding.uuid_1
	UUID_1s30 = thisbuilding.uuid_1_sub30
	UUID_1s36 = thisbuilding.uuid_1_sub36
	UUID_2 = thisbuilding.uuid_2
	UUID_2s30 = thisbuilding.uuid_2_sub30
	UUID_2s36 = thisbuilding.uuid_2_sub36
	UUID_3 = thisbuilding.uuid_3
	UUID_3s30 = thisbuilding.uuid_3_sub30
	UUID_3s36 = thisbuilding.uuid_3_sub36
	UUID_4 = thisbuilding.uuid_4
	UUID_4s30 = thisbuilding.uuid_4_sub30
	UUID_4s36 = thisbuilding.uuid_4_sub36
	UUID_5 = thisbuilding.uuid_5
	UUID_5s30 = thisbuilding.uuid_5_sub30
	UUID_5s36 = thisbuilding.uuid_5_sub36


	UUID_COUNT = 0
	for x in [UUID_0, UUID_1, UUID_2, UUID_3, UUID_4, UUID_5]:
		if x != '':
			UUID_COUNT += 1

	INFO = thisbuilding.info
	PIC = thisbuilding.pic
	STATS_SQFT = thisbuilding.stats_sqft
	STATS_YEAR = thisbuilding.stats_yearBuilt
	STATS_ALTINFO = thisbuilding.stats_altInfo

	return render_to_response('buildingpage.html', locals())
