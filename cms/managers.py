from django.conf import settings
from django.db import models

from django.contrib.sites.shortcuts import get_current_site


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def published(self):
        return self.get_queryset().filter(status='public')
    
    def published_on_site(self, request):
        return self.published().filter(site=get_current_site(request))
    
    def unpublished(self):
        return self.get_queryset().filter(status='unpublish')
    
    def unpublished_on_site(self, request):
        return self.unpublished().filter(site=get_current_site(request))
    
    def drafts(self):
        return self.get_queryset().filter(status='draft')
    
    def drafts_on_site(self, request):
        return self.drafts().filter(site=get_current_site(request))