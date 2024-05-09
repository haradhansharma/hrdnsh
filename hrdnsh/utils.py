import os
import glob
from django.core.cache.backends.filebased import FileBasedCache

class CustomFileCache(FileBasedCache):
    def _write_content(self, file, timeout, value):
        os.chmod(file, 0o666)
        super()._write_content(file, timeout, value)
   
        

