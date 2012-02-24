# Create your views here.

from django.shortcuts import render_to_response
from campenport.contact.forms import ContactForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from campenport.buildings.models import Building

def contact(request, buildnameC):
    if buildnameC=="General Site":
        building_name_in = "General Site"
    else:
        correctbuilding = Building.objects.filter(shortname=buildnameC)
        building_name_in = correctbuilding[0].longname
    buildings = Building.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('contact_form.html', locals())

def contact2(request):
	return contact(request, "General Site")

def contactThanks(request):
	buildings = Building.objects.all()
	return render_to_response('contact_thanks.html', locals())
