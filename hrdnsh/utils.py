import os
import glob
from django.core.cache.backends.filebased import FileBasedCache

class CustomFileCache(FileBasedCache):
    def _createdir(self):      
        super()._createdir()  
        old_umask = os.umask(0o000) 
        os.chmod(self._dir, 0o770)
        os.umask(old_umask)
        
    # def _list_cache_files(self):        
    #     list_of_file = [os.path.join(self._dir, fname) for fname in glob.glob1(self._dir, "*%s" % self.cache_suffix)]
    #     for f in list_of_file:     
    #         os.chmod(f, 0o666)     
    #     return list_of_file
        

