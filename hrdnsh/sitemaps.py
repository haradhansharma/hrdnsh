from datetime import datetime
from django.contrib import sitemaps
from django.urls import reverse
from cms.models import *
from common.models import *
from service.models import *
from project.models import *
from contact.models import *
from django.conf import settings
from django.utils import timezone
from django.db.models import Count


class StaticSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'weekly'

    def items(self):
        return ['common:home', 'common:about', 'cms:blog_list', 'contact:home', 'project:home', 'service:home'] 
    
    def lastmod(self, obj):
        return timezone.now()
        
    def location(self, item):
        return reverse(item)   
    
class BlogSitemap(sitemaps.Sitemap):
    def __init__(self, request):
        self.request = request
        super().__init__()
        
    changefreq = "weekly"
    priority = 0.8    

    def items(self):
        return list(Blog.status_objects.published_on_site(self.request))[-100:]
    
    def lastmod(self, obj):
        return obj.updated_at
        
    def location(self, obj):       
        return obj.get_absolute_url()
    
class PageSitemap(sitemaps.Sitemap):
    def __init__(self, request):
        self.request = request
        super().__init__()
        
    changefreq = "weekly"
    priority = 0.8    

    def items(self):
        return list(Page.status_objects.published_on_site(self.request))[-100:]
    
    def lastmod(self, obj):
        return obj.updated_at
        
    def location(self, obj):
        return obj.get_absolute_url()
    
class CategoryBlogsSitemap(sitemaps.Sitemap):
    def __init__(self, request):
        self.request = request
        super().__init__()
    changefreq = "weekly"
    priority = 0.7    

    def items(self):
        categories = list(Category.on_site.prefetch_related('blog_category').all())[-100:]
        list_cat = []
        for cate in categories:     
            list_cat.append(cate)
        return list_cat
    
    def lastmod(self, obj):
        return obj.updated_at
        
    def location(self, obj):
        return obj.get_absolute_url()
    
class TagBlogsSitemap(sitemaps.Sitemap):
    def __init__(self, request):
        self.request = request
        super().__init__()
    changefreq = "weekly"
    priority = 0.7    

    def items(self):
        tags = list(Tag.on_site.prefetch_related('blog_related'))[-100:]
        list_tag = []
        for tag in tags:    
            list_tag.append(tag)
        return list_tag
    
    def lastmod(self, obj):
        return timezone.now()
        
    def location(self, obj):
        return obj.get_tag_blogs_url()
    
class ProjectSitemap(sitemaps.Sitemap):
    def __init__(self, request):
        self.request = request
        super().__init__()
        
    changefreq = "weekly"
    priority = 0.8    

    def items(self):
        return list(Project.status_objects.published_on_site(self.request))[-100:]
    
    def lastmod(self, obj):
        return obj.updated_at
        
    def location(self, obj):
        return obj.get_absolute_url()
    
class CategoryProjectSitemap(sitemaps.Sitemap):
    def __init__(self, request):
        self.request = request
        super().__init__()
    changefreq = "weekly"
    priority = 0.7    

    def items(self):
        categories = list(Category.on_site.prefetch_related('project_categories').all())[-100:]
        list_cat = []
        for cate in categories:       
            list_cat.append(cate)
        return list_cat
    
    def lastmod(self, obj):
        return obj.updated_at
        
    def location(self, obj):
        return obj.get_projectcat_absolute_url()
    
    
class ServiceSitemap(sitemaps.Sitemap):
    def __init__(self, request):
        self.request = request
        super().__init__()
        
    changefreq = "weekly"
    priority = 0.8    

    def items(self):
        return list(Service.status_objects.published_on_site(self.request))[-100:]
    
    def lastmod(self, obj):
        return obj.updated_at
        
    def location(self, obj):
        return obj.get_absolute_url()

    

    

    

    

               
    