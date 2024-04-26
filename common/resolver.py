from django.core.cache import cache
from django.contrib.sites.models import Site

def check_host(host, request, **kwargs): 
    host = cache.get("hrdnsh_host")
    if host:
        return True
    elif Site.objects.filter(domain=host).exists():
        cache.set("hrdnsh_host", host, 3000)      
        return True
    return False