import os
import glob
from django.core.cache.backends.filebased import FileBasedCache

class CustomFileCache(FileBasedCache):        
    def has_key(self, key, version=None):
        fname = self._key_to_file(key, version)
        os.chmod(fname, 0o666)
        super().has_key(key, version)
   
        

