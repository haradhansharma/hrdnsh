from django.contrib import sitemaps
from django.urls import reverse
from card.models import *

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['card:index', 'card:cards', 'card:experiences','card:workss','card:contact', ]

    def location(self, item):
        return reverse(item)      
    
class CvSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Card.objects.all() 
    
    def lastmod(self, obj):
        return obj.created
        
    def location(self, obj):
        return "/cv/%s"  % (obj.slug)
    
class ExperienceSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Experience.objects.all() 
    
    def lastmod(self, obj):
        return obj.created   
        
    def location(self,obj):
        return '/experience/%s' % (obj.slug)    
    
class WorksSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Works.objects.all()  
    
    def lastmod(self, obj):
        return obj.created  
        
    def location(self,obj):
        return '/works/%s' % (obj.slug)  
    
class WorksTagSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Works.objects.all()  
    
    def lastmod(self, obj):
        return obj.created  
        
    def location(self,obj):
        tag = obj.Tag.all()
        for t in tag:
            return '/works/tag/%s' % (t.slug)   
    
class ServiceSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Service.objects.all()  
    
    def lastmod(self, obj):
        return obj.created  
        
    def location(self,obj):
        return '/service/request/%s' % (obj.slug)   
    
 
      
               
    