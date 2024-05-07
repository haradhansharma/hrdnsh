from pathlib import Path
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
        host = request.get_host()
        if host in SITE_CACHE_GLOBAL and f'{host}_template' in SITE_CACHE_GLOBAL:
            request.site = SITE_CACHE_GLOBAL[host]            
        else:
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
                            site = Site.objects.get(domain__iexact=host)
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
        
    

        
      
        




        
      