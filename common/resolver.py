from django.core.cache import cache
from django.contrib.sites.models import Site

def check_host(host, request, **kwargs): 
    if host.startswith('www.'):
        hosts = [host, host.replace('www.', '')]
    else:
        hosts = [host, 'www.'+host]

    hosts = cache.get("valid_hostnames")
    if hosts:
        return True
    elif Site.objects.filter(domain__in=hosts).exists():
        cache.set("valid_hostnames", hosts, 3000)      
        return True
    return False