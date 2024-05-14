from django.conf import settings
from django.db import models

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

class Project(  
    SlugMixin,   
    ImageMixin,
    DateTimeMixin,
    StatusMixin,
    SaveAndImageOptimizationMixin, #if need to edit save method look here    
    models.Model,
    
    ):    
    title = models.CharField(max_length=255)   
    summary = models.TextField(max_length=400)
    categories = models.ManyToManyField('cms.Category', blank=True, related_name='%(class)s_categories')  
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)s_site')
    view = GenericRelation(View)
    
    objects = models.Manager()  
    on_site = CurrentSiteManager('site')
    status_objects = PublishManager()
    
    image_fields_to_optimize = ['main_image']
    
    def get_absolute_url(self):        
        return reverse('project:details', args=[self.slug]) 
    
    def increment_view_count(self): 
        view, create = self.view.get_or_create(content_type = self, object_id=self.id)
        view.count += 1
        view.save()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at', 'title']
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    
class ProjectRequirement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_requirements")
    item = models.CharField(max_length=250)
    
    def __str__(self):
        return f'ID {self.id} of {self.project.title}'
    
    class Meta:
        ordering = ['item']
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    
class ProjectScoope(DateTimeMixin, models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_scoopes")
    step = models.PositiveIntegerField(help_text='Integer accepted')
    scoope = models.TextField()
    outcome = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'Step {self.step} of {self.project.title}'
    
    class Meta:
        ordering = ['step']
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    
class ScoopVisualization(
    ImageMixin, 
    SaveAndImageOptimizationMixin, #if need to edit save method look here
    models.Model
    ):
    # site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)s_site')
    project_scoope = models.ForeignKey(ProjectScoope, on_delete=models.CASCADE, related_name="scoope_visualization")    
    image_fields_to_optimize = ['main_image']
    
    class Meta:
        ordering = ['pk']
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    
    
    
    

    
