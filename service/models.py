from django.db import models
from django.contrib.sites.managers import CurrentSiteManager
from django.urls import reverse
from cms.managers import PublishManager
from cms.mixins import CategoryMixin, DateTimeMixin, ImageMixin, SaveAndImageOptimizationMixin, LikeViewCountMixin, SiteAutorMixin, SiteEmailMixin, SlugMixin, StatusMixin, TitleBodyMixin
from cms.models import Like, View
from common.models import SkillsAndTools
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.utils.text import slugify
from common.utils import optimize_image_for_web
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.sites.models import Site

class Service(
    TitleBodyMixin,
    SlugMixin,   
    ImageMixin, 
    DateTimeMixin,  
    CategoryMixin, 
    StatusMixin,
    SaveAndImageOptimizationMixin, #if need to edit save method look here
    models.Model,
    
    ): 
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)s_site')
    summary = models.TextField(max_length=400)
    skills = models.ManyToManyField(SkillsAndTools, related_name='service_skills')  
    buy_link = models.URLField(null=True, blank=True, help_text='buy link from any payment gateway')
    
    view = GenericRelation(View)
    
    objects = models.Manager()  
    on_site = CurrentSiteManager('site')
    status_objects = PublishManager()
    
    image_fields_to_optimize = ['main_image']
    
    def get_absolute_url(self):        
        return reverse('service:details', args=[self.slug]) 
    
    def increment_view_count(self): 
        view, create = self.view.get_or_create(content_type = self, object_id=self.id)
        view.count += 1
        view.save()
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    
