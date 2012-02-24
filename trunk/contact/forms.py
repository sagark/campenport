from django.forms import ModelForm
from campenport.contact.models import ContactResp

class ContactForm(ModelForm):
	class Meta:
		model = ContactResp
    
