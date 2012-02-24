from django.contrib import admin
from campenport.buildings.models import Building
from campenport.contact.models import ContactResp
#contains all admin configs, move this somewhere more suitable eventually



class BuildingAdmin(admin.ModelAdmin):
	list_display = ('longname', 'queryid', 'stats_sqft', 'stats_yearBuilt', 'pic', 'map_coords')
	ordering = ('longname',)

class ContactRespAdmin(admin.ModelAdmin):
	def get_readonly_fields(self, request, obj=None):
		return ('time', 'rBuilding', 'emailID', 'suggestion')
	list_display = ('time', 'rBuilding', 'emailID')
	ordering = ('time',)

admin.site.register(Building, BuildingAdmin)
admin.site.register(ContactResp, ContactRespAdmin)
