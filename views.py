from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from campenport.buildings.models import Building

####NOTE: for searchbox autocomplete to work, each view MUST have buildings = Building.objects.all() (also, sorting is done in the django code embedded in html so no order_by necessary here)

def homemap(request):
	buildings = Building.objects.all()	
	return render_to_response('campusmap.html', locals())

def passhome(request):
	return redirect('/map/')

def buildinglist(request):
	buildings = Building.objects.all()
	for building in buildings:
		if building.kWhqueryid == None or building.kWhqueryid == "":
			building.kWhqueryid = building.longname
		if building.rmsDev == '0' or building.rmsDev == '0.0':
			building.rmsDev = 'No Baseline'
			building.rmsPercentErr = 'No Baseline'
		else:
			building.rmsPercentErr = building.rmsPercentErr + "%"

	return render_to_response('buildinglist.html', locals())

def campus(request):
	buildings = Building.objects.all()
	BUILDING_COUNT = len(buildings)
	ACTUAL_BUILDING_COUNT = 138
	BUILD_PERCENT = round(BUILDING_COUNT/(ACTUAL_BUILDING_COUNT+0.0)*100)
	return render_to_response('campus.html', locals())

def search(request):
	buildings = Building.objects.all()
	namequery = request.GET.get('name', '')
	sqftquery = request.GET.get('sqft', '')
	yearquery = request.GET.get('year', '')
	textoutput = ''
	for query in [namequery, sqftquery, yearquery]:
		if len(textoutput)>0 and query:
			textoutput += ' and '
			textoutput += query
		else:
			textoutput += query
	if namequery or sqftquery or yearquery:
		NEW_TITLE = "Search for: " + textoutput
		qset = (
			Q(longname__icontains=namequery) & Q(stats_sqft__icontains=sqftquery) & Q(stats_yearBuilt__icontains=yearquery)
		)
		results = Building.objects.filter(qset).distinct()
	else:
		NEW_TITLE = "Search"
	return render_to_response('searchpage.html', locals())

def comparebuildings(request):
	buildings = Building.objects.order_by("longname")
	currid = 1
	for building in buildings: #gets kWh queryids
		if building.kWhqueryid == None or building.kWhqueryid == "":
			building.kWhqueryid = building.longname
			
	
	return render_to_response('compare.html', locals())
