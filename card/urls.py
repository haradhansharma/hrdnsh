from django.contrib.sitemaps.views import sitemap
from django.urls import path
from . import views
from card.sitemaps import *

sitemaps = {
    'static': StaticViewSitemap,
    'experiencesitemap': ExperienceSitemap,
    'workssitemap': WorksSitemap,
    'cvsitemap': CvSitemap,  
    'servicesitemap': ServiceSitemap,
    'workstagsitemap': WorksTagSitemap
    
}

app_name = 'card'
urlpatterns = [
    path('', views.index, name='index'),
    path('cards/', views.CardListView.as_view(), name='cards'),
    path('cv/<str:slug>/', views.CardDetailView.as_view(), name='card-detail'),
    path('experiences/', views.ExperienceListView.as_view(), name='experiences'), 
    path('experience/<slug:slug>/', views.ExperienceDetailView.as_view(), name='experience-detail'),     
    path('workss/', views.works_list_view, name='workss'), 
    path('works/<slug:slug>/', views.WorksDetailView.as_view(), name='works-detail'), 
    path('contact/', views.ContactView, name='contact'),
    path('service/request/<slug:slug>/', views.service_detail_view, name='service-request'),
    path('works/tag/<str:tag>', views.tag_detail, name="tag" ),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),    
]