from django.db import models

# Create your models here.
#what is needed:
"""
building shortname (what is in the url) ie. cory
building longname (official name) ie. Cory Hall
building source UUID
building building information
building picture
building stats
	SQ Ft
	Year built
	info paragraph
	Materials
	Number of Windows

Later, replace hardcoded UUID storage with tags
"""

class Building(models.Model):
	shortname = models.CharField(max_length=50)
	longname = models.CharField(max_length=100)
	queryid = models.CharField(max_length=100, blank=True)
	sumQueryid = models.CharField(max_length=100, blank=True)
	kWhqueryid = models.CharField(max_length=100, blank=True)
	map_coords = models.CharField(max_length=2000)
	info = models.CharField(max_length=2000, blank=True)
	pic = models.CharField(max_length=2000, blank=True)
	pic_src = models.CharField(max_length=2000, blank=True)
	stats_sqft = models.CharField(max_length=20, blank=True)
	stats_yearBuilt = models.CharField(max_length=4, blank=True)
	stats_altInfo = models.CharField(max_length=2000, blank=True)
	rmsDev = models.CharField(max_length=50, default=0)
	rmsPercentErr = models.CharField(max_length=50, default=0)
	peak_avg = models.CharField(max_length=50, default=0)
	
	def __str__(self):
		return '%s' % self.longname
