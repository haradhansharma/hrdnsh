from django.apps import AppConfig

from django.conf import settings

class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    
    def ready(self):
        pass
