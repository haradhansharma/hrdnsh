from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
class Contact(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()  
    on_site = CurrentSiteManager('site')

    def __str__(self):
        return self.name
