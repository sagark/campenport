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
	query = request.GET.get('name', '')
	if query:
		NEW_TITLE = "Search for: " + query
		qset = (
			Q(longname__icontains=query)
		)
		results = Building.objects.filter(qset).distinct()
	else:
		NEW_TITLE = "Search"
	return render_to_response('searchpage.html', locals())
