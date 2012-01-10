from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from campenport.buildings.models import Building

def homemap(request):
	buildings = Building.objects.all()	
	return render_to_response('campusmap.html', locals())

def newhomemap(request):
	buildings = Building.objects.all()
	return render_to_response('newcampusmap.html', locals())

def passhome(request):
	return HttpResponseRedirect('/map/')

def map2(request):
	image_data = open("templates/campusmap.png", "rb").read()
	return HttpResponse(image_data, mimetype="image/png")

