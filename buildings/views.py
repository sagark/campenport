from django.shortcuts import render_to_response
from campenport.buildings.models import Building
from campenport.settings import CMAPheight, CMAPwidth
####NOTE: for searchbox autocomplete to work, each view MUST have buildings = Building.objects.all() (also, sorting is done in the django code embedded in html so no order_by necessary here)


def buildings(request, buildname):
	buildings = Building.objects.all()
	SHORT_NAME = buildname
	try:
		thisbuilding = Building.objects.get(shortname = SHORT_NAME)
	except:
		ERR_BUILD = SHORT_NAME
		return render_to_response('buildingDNE.html', locals())

	BUILDING_NAME = thisbuilding.longname #required

	if thisbuilding.queryid == None or thisbuilding.queryid == '': #for smap query, use building id if not special
		QUERY_ID = BUILDING_NAME
	else:
		QUERY_ID = thisbuilding.queryid

	
	#generate the box that allows viewing map location
	coordfull = thisbuilding.map_coords
	coordfull = coordfull.split(',')
	outp_x = []
	outp_y = []
	for x in range(len(coordfull)):
		if x%2 == 0:
			outp_x.append(int(coordfull[x]))
		else:
			outp_y.append(int(coordfull[x]))
	x_max = 0
	x_min = 9999999999
	y_max = 0
	y_min = 9999999999
	desired_width = 450
	desired_height = 300
	for x in outp_x:
		if x > x_max:
			x_max = x
		elif x < x_min:
			x_min = x
	for y in outp_y:
		if y > y_max:
			y_max = y
		elif y < y_min:
			y_min = y
	buildingwidth = x_max - x_min
	buildingheight = y_max - y_min
	subwidth = (desired_width - buildingwidth)/2
	subheight = (desired_height - buildingheight)/2
	x_min -= subwidth
	y_min -= subheight

	
	#the following uuid count needs to now be implemented in js instead
	#UUID_COUNT = 0
	#for x in [UUID_0, UUID_1, UUID_2, UUID_3, UUID_4, UUID_5]:
	#	if x != '':
	#		UUID_COUNT += 1

	INFO = thisbuilding.info
	PIC = thisbuilding.pic
	PIC_SRC = thisbuilding.pic_src
	STATS_SQFT = thisbuilding.stats_sqft
	STATS_YEAR = thisbuilding.stats_yearBuilt
	STATS_ALTINFO = thisbuilding.stats_altInfo

	return render_to_response('buildingpage.html', locals())
