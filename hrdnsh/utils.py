import os
from django.utils.crypto import md5
from django.core.cache.backends.filebased import FileBasedCache

class CustomFileCache(FileBasedCache):    
  
        
    def _key_to_file(self, key, version=None):
        
        key = self.make_and_validate_key(key, version=version)
        file = os.path.join(
            self._dir,
            "".join(
                [
                    md5(key.encode(), usedforsecurity=False).hexdigest(),
                    self.cache_suffix,
                ]
            ),
        )
        os.chmod(file, 0o666)
        return file
   
        

