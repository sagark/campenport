from django.db import models

# Create your models here.

class ContactResp(models.Model):
	suggestion = models.TextField()
	emailID = models.EmailField(blank=True)
	rBuilding = models.CharField(max_length=100)
	time = models.DateTimeField(auto_now_add=True)
	
	
