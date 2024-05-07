from pathlib import Path
from django.http import HttpResponsePermanentRedirect
import environ
import os
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sites.models import Site
from django.http.request import split_domain_port
from django.template import TemplateDoesNotExist
import threading


from common.loader import CustomLoader

import logging
log =  logging.getLogger('log')

SITE_CACHE_GLOBAL = {}
SITE_CACHE_OWN_LOCK = threading.Lock()

def modify_site_cache_global():
    global SITE_CACHE_GLOBAL
    SITE_CACHE_GLOBAL = {}

class DynamicSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(CustomLoader, 'request', request)
        self.set_site_id(request)
        response = self.get_response(request)
        return response
    
    def _template_exists(self, template):
        template_path = os.path.join(settings.BASE_DIR, settings.TEMP_DIR, template)   
        if os.path.exists(template_path):
            return True
        return False       
        

    def set_site_id(self, request):
        host = request.get_host().lower()
        log.info(f'host is ________{host}')
        #redirect to https
        if not request.is_secure() or host.startswith('www.'):
            log.info(f'request is not secure ________')
            if host.startswith('www.'):
                log.info(f'start with www. ________')
                new_host = host[4:]
                url = f"https://{new_host}{request.path}"
                log.info(f'new url build {url} ________')
                return HttpResponsePermanentRedirect(url)       
        
        log.info(f'checking host in __________________ {SITE_CACHE_GLOBAL}')
        if host in SITE_CACHE_GLOBAL and f'{host}_template' in SITE_CACHE_GLOBAL:
            log.info(f'host found in cache ________')
            request.site = SITE_CACHE_GLOBAL[host]            
        else:
            log.info(f'{host} not found in cache ________')
            with SITE_CACHE_OWN_LOCK:
                if host not in SITE_CACHE_GLOBAL:
                    try:
                        site = Site.objects.get(domain__iexact=host)
                        SITE_CACHE_GLOBAL[host] = site         
                                       
                        try:
                            template = site.profile.selected_template.template.template_dir                            
                            if not self._template_exists(template):
                                template = settings.DEFAULT_TEMPLATE                                                            
                        except:
                            template = settings.DEFAULT_TEMPLATE
                            
                        SITE_CACHE_GLOBAL[f'{host}_template'] = template
                        
                    except Site.DoesNotExist:
                        
                        domain, port = split_domain_port(host)
                        if domain not in SITE_CACHE_GLOBAL:
                            site = Site.objects.get(domain__iexact=domain)
                            SITE_CACHE_GLOBAL[domain] = site    
                                                    
                            try:
                                template = site.profile.selected_template.template.template_dir
                                if not self._template_exists(template):
                                    template = settings.DEFAULT_TEMPLATE     
                            except:
                                template = settings.DEFAULT_TEMPLATE     
                                                           
                            SITE_CACHE_GLOBAL[f'{domain}_template'] = template
                            
                    except Exception as e:                        
                        log.warning(f'Template Issue: {e}')
                                    
        request.site = SITE_CACHE_GLOBAL.get(host)
        settings.SITE_ID = request.site.id if request.site else 1        
        request.CURRENT_TEMPLATE = SITE_CACHE_GLOBAL.get(f'{host}_template')
        
    

        
      
        




        
      