from django.urls import include, path

from hdapi.views import (  
        CmsBlogViewSet,
        CmsCategoryViewSet,
        CmsPageViewSet,
        CmsTagViewSet,
        ContentTypeCommentViewSet,
        ContentTypeViewSet,
        DecoratedTokenBlacklistView, 
        DecoratedTokenObtainPairView, 
        DecoratedTokenRefreshView, 
        DecoratedTokenVerifyView,
        ExperienceWhatDidViewSet,
        ExtraProfileImagesViewSet,
        GroupViewSet,
        KeyQualificationViewSet,
        PersonalizedEmailSettingViewSet,
        ProfileTemplateViewSet,
        ProjectRequirementViewSet,
        ProjectScoopeViewSet,
        ProjectViewSet,
        ScoopVisualizationViewSet,
        ServiceViewSet,
        SiteExperienceViewSet,
        SiteProfileViewSet,   
        SiteViewSet,
        UserViewSet,        
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.routers import DefaultRouter
schema_view_v1 = get_schema_view(
    openapi.Info(
        title="HRDHSN SaaS API",
        default_version='v1',
        description="API for managing Profile as SaaS",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="haradhan.sharma@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = 'hdapi'

router = DefaultRouter()
router.register('common_sites', SiteViewSet)
'''
# one to one related to the site 
# creating while creating site
# So retrive, update, partial update and destroy implemented
'''
router.register('common_sites/profile', SiteProfileViewSet, basename='profile')
router.register('common_sites/profile/template', ProfileTemplateViewSet, basename='profile-template')
router.register('common_sites/personalized_email_settings', PersonalizedEmailSettingViewSet, basename='site-prsonalized-email-settings')

router.register(r'common_sites/profile/(?P<profile_pk>\d+)/extra_profile_images', ExtraProfileImagesViewSet, basename='profile-extra-images')

router.register(r'common_sites/(?P<site_pk>\d+)/experiences', SiteExperienceViewSet, basename='site-experience')
router.register(r'common_sites/(?P<site_pk>\d+)/experiences/(?P<experience_pk>\d+)/what_did', ExperienceWhatDidViewSet, basename='experience-whatdid')
router.register(r'common_sites/(?P<site_pk>\d+)/experiences/(?P<experience_pk>\d+)/skills_and_tools', ExperienceWhatDidViewSet, basename='experience-skills-and-tools')
router.register(r'common_sites/(?P<site_pk>\d+)/key_qualification', KeyQualificationViewSet, basename='site-key-qualification')

router.register(r'cms_site/(?P<site_pk>\d+)/tags', CmsTagViewSet, basename='csm-site-tags')
router.register(r'cms_site/(?P<site_pk>\d+)/category', CmsCategoryViewSet, basename='csm-site-categories')
router.register(r'cms_site/(?P<site_pk>\d+)/blogs', CmsBlogViewSet, basename='csm-site-blogs')
router.register(r'cms_site/(?P<site_pk>\d+)/pages', CmsPageViewSet, basename='csm-site-pages')


router.register(r'project_site/(?P<site_pk>\d+)/projects', ProjectViewSet, basename='project-site-projects')
router.register(r'project_site/(?P<site_pk>\d+)/projects/(?P<project_pk>\d+)/project_requirements', ProjectRequirementViewSet, basename='project-requirements')
router.register(r'project_site/(?P<site_pk>\d+)/projects/(?P<project_pk>\d+)/project_scoopes', ProjectScoopeViewSet, basename='project-scoopes')
router.register(r'project_site/(?P<site_pk>\d+)/projects/(?P<project_pk>\d+)/project_scoopes/(?P<scoope_pk>\d+)/visualizations', ScoopVisualizationViewSet, basename='project-scoopes-visualizations')

router.register(r'service_site/(?P<site_pk>\d+)/services', ServiceViewSet, basename='service-site-services')


router.register(r'content_type', ContentTypeViewSet, basename='content-types')
router.register(r'content_type/(?P<content_type_pk>\d+)/object/(?P<object_pk>\d+)/comments', ContentTypeCommentViewSet, basename='content-types-comments')


router.register(r'users', UserViewSet, basename='user')
router.register(r'users/groups', GroupViewSet, basename='user-group')









urlpatterns = [
    path('', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),    
    path('hdapi.json/', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    
    
    path('token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', DecoratedTokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', DecoratedTokenBlacklistView.as_view(), name='token_blacklist'),    
    
    path('', include(router.urls)),
    

    

]








