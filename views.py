from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from campenport.buildings.models import Building

def homemap(request):
	buildings = Building.objects.all()	
	return render_to_response('campusmap.html', locals())

def passhome(request):
	return HttpResponseRedirect('/map/')

def buildinglist(request):
	buildings = Building.objects.all()
	return render_to_response('buildinglist.html', locals())

def search(request):
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
	for building in buildings: #normalizes square footage data for display
		if building.stats_sqft == '':
			building.stats_sqft_fordisp = '50'
		else:
			building.stats_sqft_fordisp = str(int(building.stats_sqft)/1000)

		if currid%2 == 0: #for zebra-striping bars
			building.tempid = False
		else:
			building.tempid = True
		currid += 1

	return render_to_response('compare.html', locals())
