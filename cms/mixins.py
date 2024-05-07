import os
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.db import transaction
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from common.utils import optimize_image_for_web
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

User = get_user_model()

def get_upload_path(instance, filename):
    # Construct the upload path dynamically using the instance's class name
    class_name = instance.__class__.__name__.lower()
    return os.path.join(f"{class_name}_images", filename)


class LikeViewCountMixin(models.Model):
    
    likes = GenericRelation('cms.Like')
    views = GenericRelation('cms.View')

    class Meta:
        abstract = True

class CommentMixin(models.Model):
    comments = GenericRelation('cms.Comment')
    
    class Meta:
        abstract = True     
        
        
class SlugMixin(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'title'):
            raise ImproperlyConfigured("Title field is required to use this SlugMixin")  
        if not issubclass(self.__class__, SaveSlugMixin): 
            if not issubclass(self.__class__, SaveAndImageOptimizationMixin):
                raise ImproperlyConfigured("SlugMixin must be used with SaveSlugMixin")  
    slug = models.SlugField(max_length=255, unique=True)
    
    class Meta:
        abstract = True 
    
    
class DateTimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True   
        
class StatusMixin(models.Model):
    status = models.CharField(max_length=10, choices=(('public', 'Public'), ('unpublish', 'Unpublish'), ('draft', 'Draft')), default="draft")
    
    class Meta:
        abstract = True 
        
class TitleBodyMixin(models.Model):
    title = models.CharField(max_length=255)   
    body = models.TextField()
    
    class Meta:
        abstract = True       

# Mixin for common fields
class SiteAutorMixin(models.Model):   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not issubclass(self.__class__, SaveSlugMixin): 
            if not issubclass(self.__class__, SaveAndImageOptimizationMixin):
                raise ImproperlyConfigured("SiteAutorMixin must be used with SaveSlugMixin")  
        if issubclass(self.__class__, SiteEmailMixin):
            raise ImproperlyConfigured("Any one can be used from SiteEmailMixin and SiteAutorMixin")     
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)s_site')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_author')    

    class Meta:
        abstract = True   
        
class SiteEmailMixin(models.Model):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        if issubclass(self.__class__, SiteAutorMixin):
            raise ImproperlyConfigured("Any one can be used from SiteEmailMixin and SiteAutorMixin")      
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)s_site')
    email = models.EmailField()    

    class Meta:
        abstract = True       
            
            
class ImageMixin(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not issubclass(self.__class__, SaveAndImageOptimizationMixin):
            raise ImproperlyConfigured("ImageMixin must be used with SaveAndImageOptimizationMixin to process thumbnail image")        
    main_image = models.ImageField(upload_to=get_upload_path)
    thumbnail_image = models.ImageField(upload_to=get_upload_path, editable=False)
    
    class Meta:
        abstract = True   
        
        
class SaveSlugMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'title'):
            raise ImproperlyConfigured("Title field is required to use this SaveSlugMixin")  
            
        if issubclass(self.__class__, SaveAndImageOptimizationMixin):
            raise ImproperlyConfigured("SaveSlugMixin is not required as here SaveAndImageOptimizationMixin applied")  
        
    def save(self, *args, **kwargs):          
        if hasattr(self, 'slug') and not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)
    
            

class SaveAndImageOptimizationMixin:  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        
        
        if not hasattr(self, 'image_fields_to_optimize'):
            raise ImproperlyConfigured("Please define image_fields_to_optimize property list")
        
        if not isinstance(self.image_fields_to_optimize, list):
            raise ImproperlyConfigured("image_fields_to_optimize must be a list")
        
         
    def save(self, *args, **kwargs):    
        is_new_instance = self._state.adding

        if not is_new_instance:
            old_instance = self.__class__.objects.get(pk=self.pk)
        else:
            old_instance = None       
                
        if hasattr(self, 'title') and hasattr(self, 'slug') and not self.slug:
            self.slug = generate_unique_slug(self, self.title)
            
            
        super().save(*args, **kwargs)       # we need to save image to go to the next operation
     
        
        # main_image = getattr(self, 'main_image', None)         
        if hasattr(self, 'main_image') :
            new_image_name = slugify(f'{self.site.domain}--{self.__class__.__name__}--thumb--{self.pk}')  
            if is_new_instance:                     
                optimized_thumbnail = optimize_image_for_web(self.main_image.path, delete_original=False, width=450, new_name=new_image_name)          
                self.thumbnail_image = optimized_thumbnail          
                super().save(*args, **kwargs)  
            
            if old_instance:
                if self.main_image != old_instance.main_image:
                    optimized_thumbnail = optimize_image_for_web(self.main_image.path, delete_original=False, width=450, new_name=new_image_name)  
                    self.thumbnail_image = optimized_thumbnail                  
                    old_instance.thumbnail_image.delete(save=False)             
                    super().save(*args, **kwargs)          
        
        image_fields = getattr(self, 'image_fields_to_optimize', [])                
        
  
        changed_fields = self._process_image_fields(old_instance, image_fields)
        
        # Save the instance again if any image fields were optimized
        if changed_fields:
            super().save(*args, **kwargs)
        
            
            
            
    
    
        
    def _process_image_fields(self, old_instance, image_fields):
        changed_fields = []
        for field_name in image_fields:
            if old_instance is not None:                
                old_image_field = getattr(old_instance, field_name)
                new_image_field = getattr(self, field_name)
                if old_image_field != new_image_field:                
                    if new_image_field:  
                        print('189 deleting') 
                        old_image_field.delete(save=False)                                         
                        optimized_webp = self._optimize_image(field_name, new_image_field)                                 
                        setattr(self, field_name, optimized_webp) 
                        changed_fields.append(field_name)                   
            else: 
                image_field = getattr(self, field_name, None)           
                if image_field is not None:   
                    optimized_webp = self._optimize_image(field_name, image_field)    
                    setattr(self, field_name, optimized_webp)  
                    changed_fields.append(field_name)
        return changed_fields

    def _optimize_image(self, field_name, image_field):
        new_image_name = slugify(f'{self.site.domain}--{self.__class__.__name__}-{field_name}-{self.pk}')             
        optimized_webp = optimize_image_for_web(image_field.path, delete_original=True, new_name=new_image_name)    
        
        return  optimized_webp
            
        
def generate_unique_slug(cls, title):        
        slug = slugify(title)
        unique_slug = slug
        num = 1
        while cls.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug       

            
# Mixin for tagging
class TaggingMixin(models.Model):
    tags = models.ManyToManyField('cms.Tag', blank=True, related_name='%(class)s_related')

    class Meta:
        abstract = True
        
        
        
class CategoryMixin(models.Model):
    category = models.ForeignKey('cms.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_category')  
    
    class Meta:
        abstract = True