import os
from django.core.cache.backends.filebased import FileBasedCache

class CustomFileCache(FileBasedCache):
    def _createdir(self):      
        super()._createdir()  
        os.chmod(self._dir, 0o700) 
