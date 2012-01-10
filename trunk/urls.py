from django.conf.urls.defaults import *
from campenport.views import homemap, map2, newhomemap
import campenport.settings as settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'campenport.views.passhome'),
	(r'^map/$', homemap),
	(r'^newmap/$', newhomemap), #testing bootstrap interface, not currently default
	(r'^map/campusmap.png', map2),
	(r'^buildings/(?P<buildname>[a-zA-Z0-9_.-]+)/$', 'campenport.buildings.views.buildings'),
	(r'^ARDgetData/', include('campenport.ARDgetData.urls')),
	(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.SITE_MEDIA + '/site-media/'}),
	(r'^admin/', include(admin.site.urls)),
)
