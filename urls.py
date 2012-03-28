from django.conf.urls.defaults import *
from campenport.views import homemap, buildinglist, search, comparebuildings, campus
from campenport.contact.views import contact, contactThanks, contact2
import campenport.settings as settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'campenport.views.passhome'),
	(r'^map/$', homemap),
	(r'^api/$', include('campenport.api.urls')),
	(r'^buildlist/$', buildinglist),
	(r'^compare/$', comparebuildings),
	(r'^campus/$', campus),
	(r'^buildings/(?P<buildname>[a-zA-Z0-9_.-]+)/$', 'campenport.buildings.views.buildings'),
	(r'^search/$', search),
	(r'^ARDgetData/', include('campenport.ARDgetData.urls')),
	(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.SITE_MEDIA + '/site-media/'}),
	(r'^admin/', include(admin.site.urls)),
	(r'contact/thanks/', contactThanks),
	(r'^contact/in/(?P<buildnameC>[a-zA-Z0-9_.-]+)/$', contact),
	(r'^contact/in/', contact2),
)
