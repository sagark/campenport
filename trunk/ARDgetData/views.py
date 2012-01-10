import urllib
import revproxy
import campenport.settings as settings

def proxy(request):
    return revproxy.proxy_request(request, destination=settings.ARD_URL, prefix='ARDgetData')

