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
	uuid_0 = models.CharField(max_length=36)
	uuid_0_sub30 = models.CharField(max_length=36, blank=True)
	uuid_0_sub36 = models.CharField(max_length=36, blank=True)
	uuid_1 = models.CharField(max_length=36, blank=True)
	uuid_1_sub30 = models.CharField(max_length=36, blank=True)
	uuid_1_sub36 = models.CharField(max_length=36, blank=True)
	uuid_2 = models.CharField(max_length=36, blank=True)
	uuid_2_sub30 = models.CharField(max_length=36, blank=True)
	uuid_2_sub36 = models.CharField(max_length=36, blank=True)
	uuid_3 = models.CharField(max_length=36, blank=True)
	uuid_3_sub30 = models.CharField(max_length=36, blank=True)
	uuid_3_sub36 = models.CharField(max_length=36, blank=True)
	uuid_4 = models.CharField(max_length=36, blank=True)
	uuid_4_sub30 = models.CharField(max_length=36, blank=True)
	uuid_4_sub36 = models.CharField(max_length=36, blank=True)
	uuid_5 = models.CharField(max_length=36, blank=True)
	uuid_5_sub30 = models.CharField(max_length=36, blank=True)
	uuid_5_sub36 = models.CharField(max_length=36, blank=True)
	info = models.CharField(max_length=2000, blank=True)
	pic = models.CharField(max_length=2000, blank=True)
	pic_src = models.CharField(max_length=2000, blank=True)
	stats_sqft = models.CharField(max_length=20, blank=True)
	stats_yearBuilt = models.CharField(max_length=4, blank=True)
	stats_altInfo = models.CharField(max_length=2000, blank=True)
	
	def __str__(self):
		return '%s' % self.longname
