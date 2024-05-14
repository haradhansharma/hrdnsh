from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from common.views import webmanifest
from .sitemaps import *

def build_sitemap(request):
    sitemap_list = {
        'static': StaticSitemap,
        'blogs' : BlogSitemap(request),
        'categoryblog' : CategoryBlogsSitemap(request),
        'tagblog' : TagBlogsSitemap(request),
        'project' : ProjectSitemap(request),        
        'categoryproject' : CategoryProjectSitemap(request),
        'service' : ServiceSitemap(request),
    }
    
    return sitemap(request, sitemaps = sitemap_list)



urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('sitemap.xml', build_sitemap, name='django.contrib.sitemaps.views.sitemap'),  
    path('backdoor/', admin.site.urls),  
    
    path('summernote/', include('django_summernote.urls')), 
    path("select2/", include("django_select2.urls")), 
    path('', include('common.urls')),   
    path('account/', include('account.urls')),
    path('cms/', include('cms.urls')),
    path('contact/', include('contact.urls')),     
    path('projects/', include('project.urls')),         
    path('services/', include('service.urls')), 
    path('api/v1/', include('hdapi.urls')),    
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),      
             
        
]

urlpatterns += [    
    path('manifest.json', webmanifest, name='manifest'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
