import os
from django.conf import settings
from django.template.loaders.app_directories import Loader
import functools


class CustomLoader(Loader):
    request = None                 
    def get_dirs(self):         
        if hasattr(self.request, 'CURRENT_TEMPLATE'):                    
            dir = self.request.CURRENT_TEMPLATE     
            return get_app_template_dirs(dir) + super().get_dirs()                  
        else:       
            return super().get_dirs()        
        
@functools.lru_cache
def get_app_template_dirs(dirname):    
    template_dirs = [  
        os.path.join(settings.BASE_DIR, settings.TEMP_DIR, dirname),          
                 
    ]
    
    return tuple(template_dirs)
        
        