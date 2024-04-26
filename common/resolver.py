from django.core.cache import cache
from django.contrib.sites.models import Site

def check_host(host, request, **kwargs):
    # Check if the host starts with 'www.' and create list of possible hosts
    if host.startswith('www.'):
        hosts = [host, host.replace('www.', '')]
    else:
        hosts = [host, 'www.' + host]

    # Fetch valid_hostnames from cache
    valid_hostnames = cache.get("valid_hostnames")

    if valid_hostnames is not None:
        # If host is in valid_hostnames, return True
        if host in valid_hostnames:
            return True
    else:
        # If valid_hostnames not in cache, query database
        if Site.objects.filter(domain__in=hosts).exists():
            # If host is valid, set valid_hostnames in cache and return True
            cache.set("valid_hostnames", hosts, 3000)
            return True

    # If host is not valid or not in valid_hostnames, return False
    return False