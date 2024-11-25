from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.db import transaction
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from django.contrib.sites.managers import CurrentSiteManager
from cms.managers import PublishManager
from common.utils import optimize_image_for_web
from django.contrib.sites.shortcuts import get_current_site
from cms.mixins import (
    SaveAndImageOptimizationMixin, LikeViewCountMixin, CommentMixin, SaveSlugMixin, SiteEmailMixin, SlugMixin, DateTimeMixin, 
    StatusMixin, TitleBodyMixin, SiteAutorMixin, ImageMixin, TaggingMixin, 
    CategoryMixin
)


User = get_user_model()

# Like model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='%(class)s_likes')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

# View model
class View(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='%(class)s_views')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    count = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)

# Tag model
class Tag(models.Model): 
    name = models.CharField(max_length=50)        
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='tags')
    view = GenericRelation(View)
    
    objects = models.Manager()   
    on_site = CurrentSiteManager('site')
    
    def increment_view_count(self):   
        view, create = self.view.get_or_create(content_type = self, object_id=self.id)
        view.count += 1
        view.save()
        

        
  
   

    def __str__(self):
        return self.name
    
    def get_tag_blogs_url(self):        
        return reverse('cms:blog_tag', args=[self.id]) 
    
    class Meta:
        ordering = ['name']  
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]


    

class Comment(   
    SiteEmailMixin, 
    LikeViewCountMixin, 
    DateTimeMixin,
    models.Model
    ): 
    body = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='%(class)s_comments')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    objects = models.Manager()  
    on_site = CurrentSiteManager('site')
    
    class Meta:
        ordering = ['-created_at']
        
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
        
    def get_delete_edit_url(self):
        return reverse('cms:edit_delete_comment', args=[int(self.id)])
   

    def __str__(self):
        return f'Comment by {self.email} on {self.created_at}'
    
    def add_like(self, user): 
        like, created = Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            user=user
        )
        return created

    def remove_like(self, user):
        Like.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            user=user
        ).delete()
    
    


# Blog model
class Blog(   
    TitleBodyMixin,
    SlugMixin, 
    TaggingMixin, 
    CommentMixin, 
    ImageMixin,  
    DateTimeMixin, 
    CategoryMixin, 
    StatusMixin,
    SaveAndImageOptimizationMixin, #if need to edit save method look here
    models.Model
    
    ):   
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)s_site') 
    summary = models.TextField(max_length=400)
    footnote = models.TextField(max_length=400, null=True, blank=True)    
    view = GenericRelation(View)
    comments = GenericRelation(Comment)
    
    image_fields_to_optimize = ['main_image']
    
    objects = models.Manager()  
    on_site = CurrentSiteManager('site')
    status_objects = PublishManager()
    
    class Meta:
        ordering = ['-created_at']   

        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    
    
    def get_absolute_url(self):        
        return reverse('cms:blog_detail', args=[self.slug]) 
    
    def increment_view_count(self):   
        view, create = self.view.get_or_create(content_type = self, object_id=self.id)
        view.count += 1
        view.save()

    def add_like(self, user): 
        like, created = Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            user=user
        )
        return created

    def remove_like(self, user):
        Like.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            user=user
        ).delete()
        
    def add_comment(self, site, email, body):        
        comment_content_type = ContentType.objects.get_for_model(self)      
        comment = Comment(
            content_type=comment_content_type,
            object_id=self.id,
            email=email,
            body=body,
            site=site
        )
        comment.save()
        return comment

    def remove_comment(self, comment_id):       
        try:
            comment = self.comments.get(id=comment_id)
            comment.delete()
            return True
        except Comment.DoesNotExist:
            return False
    
    
    def __str__(self):
        return self.title
    

class Page(   
    TitleBodyMixin,
    SlugMixin,  
    ImageMixin,  
    DateTimeMixin,  
    StatusMixin,
    SaveAndImageOptimizationMixin, #if need to edit save method look here
    models.Model
    
    ):   
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)s_site') 
    summary = models.TextField(max_length=400)
    footnote = models.TextField(max_length=400, null=True, blank=True)    
    view = GenericRelation(View)
    
    image_fields_to_optimize = ['main_image']
    
    objects = models.Manager()  
    on_site = CurrentSiteManager('site')
    status_objects = PublishManager()
    
    class Meta:
        ordering = ['-created_at']   

        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    
    
    def get_absolute_url(self):        
        return reverse('page_detail', args=[self.slug]) 
    
    def increment_view_count(self):   
        view, create = self.view.get_or_create(content_type = self, object_id=self.id)
        view.count += 1
        view.save()
 
# Category model
class Category(
    TitleBodyMixin,
    SlugMixin, 
    DateTimeMixin, 
    SaveSlugMixin,
    models.Model
    ):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='categories')
    
    objects = models.Manager()  
    on_site = CurrentSiteManager('site')

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):        
        return reverse('cms:blog_category', args=[self.slug])
    
    def get_projectcat_absolute_url(self):        
        return reverse('project:project_category', args=[self.slug])
    
    def get_servicecat_absolute_url(self):        
        return reverse('service:service_category', args=[self.slug])
    
    class Meta:
        ordering = ['title']        
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    
