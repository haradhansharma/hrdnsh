import os
import glob
from django.core.cache.backends.filebased import FileBasedCache

class CustomFileCache(FileBasedCache):
    def get(self, key, default=None, version=None):
        fname = self._key_to_file(key, version)
        os.chmod(fname, 0o666) 
        super().get(key, default, version)
        
   
        

