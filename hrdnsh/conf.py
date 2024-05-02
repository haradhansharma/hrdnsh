
import os
from django.utils.functional import LazyObject
from django.conf import settings
from django.core.cache import cache

import logging
log =  logging.getLogger('log')


class LazyCurrentTemplate(LazyObject):
    def _setup(self):
        from django.apps import apps
        apps.populate(settings.INSTALLED_APPS)
        self._wrapped = self._get_static_root()

    def _get_static_root(self):        
        from common.models import SiteTemplate
        try:
            current_template = SiteTemplate.on_site.get().template_dir
            temp_dir = os.path.join(settings.TEMP_UPLOAD_DIR, current_template)     
            if not os.path.exists(temp_dir):
                log.error(f'ERROR: SITE SPECIFIC TEMPLATE {current_template} NOT FOUND ACORDING TO DATABASE RECORD! WE ARE GOING TO USE DEFAULT TEMPLATE! PLEASE UPLOAD TEMPLATE!')
                raise
        except Exception as e: 
            log.error(f'ERROR: {e}! WE ARE GOING TO USE DEFAULT TEMPLATE!')               
            current_template = 'default'          
        
        return current_template
            
        