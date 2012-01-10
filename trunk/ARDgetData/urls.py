from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^.*$', 'campenport.ARDgetData.views.proxy')
)
