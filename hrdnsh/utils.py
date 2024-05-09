import os
import glob
from django.core.cache.backends.filebased import FileBasedCache

class CustomFileCache(FileBasedCache):
    def get(self, key, default=None, version=None):        
        super().get(key, default, version)
        fname = self._key_to_file(key, version)
        os.chmod(fname, 0o666) 
        
   
        

