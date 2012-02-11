from piston.handler import BaseHandler

from campenport.buildings.models import Building

class BuildingHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = Building

