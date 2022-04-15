from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


admin.site.site_header = 'HARADHAN SHARMA admin'
admin.site.site_title = 'HARADHAN SHARMA admin'
# admin.site.site_url = 'http://gf-vp.com/'
admin.site.index_title = 'HARADHAN SHARMA administration'
# admin.empty_value_display = '**Empty**'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('card.urls')),      
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
