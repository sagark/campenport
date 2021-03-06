from django.conf.urls.defaults import *
from piston.resource import Resource
from campenport.api.handlers import BuildingHandler

buildinghandler = Resource(BuildingHandler)

urlpatterns = patterns('',
	(r'^', buildinghandler),
)
