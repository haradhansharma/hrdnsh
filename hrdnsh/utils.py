import os
import tempfile
from django.core.files.move import file_move_safe
from django.core.cache.backends.filebased import FileBasedCache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

class CustomFileCache(FileBasedCache):  
    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        self._createdir()
        fname = self._key_to_file(key, version)
        
        self._cull()
        fd, tmp_path = tempfile.mkstemp(dir=self._dir)
        os.chmod(fd, 0o666)
        renamed = False
        try:
            with open(fd, "wb") as f:
                self._write_content(f, timeout, value)
            file_move_safe(tmp_path, fname, allow_overwrite=True)
            renamed = True
        finally:
            if not renamed:
                os.remove(tmp_path)  
  
        
  
   
        

