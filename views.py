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
