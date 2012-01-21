from django.contrib import admin
from campenport.buildings.models import Building

class BuildingAdmin(admin.ModelAdmin):
	list_display = ('longname', 'queryid', 'stats_sqft', 'stats_yearBuilt', 'pic', 'map_coords')
	ordering = ('longname',)

admin.site.register(Building, BuildingAdmin)
