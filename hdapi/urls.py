from django.urls import include, path

from hdapi.views import ( 
        AllExperienceViewSet,
        CmsBlogViewSet,
        CmsCategoryViewSet,
        CmsTagViewSet,
        ContentTypeCommentViewSet,
        ContentTypeViewSet,
        DecoratedTokenBlacklistView, 
        DecoratedTokenObtainPairView, 
        DecoratedTokenRefreshView, 
        DecoratedTokenVerifyView,
        ExperienceWhatDidViewSet,
        ExtraProfileImagesViewSet,
        KeyQualificationViewSet,
        PersonalizedEmailSettingViewSet,
        ProfileTemplateViewSet,
        SiteExperienceViewSet,
        SiteProfileViewSet,
        # SelectedTemplateViewSet,
        SiteViewSet,
        # TagListCreateView,
        # TagRetrieveUpdateDestroyView,
        # TagSiteListView,
        # TagViewCount
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
router.register('sites', SiteViewSet)
# router.register('site_template/(?P<profile_id>\d+)', SelectedTemplateViewSet)
router.register('sites/profile', SiteProfileViewSet, basename='profile')
router.register('sites/profile/template', ProfileTemplateViewSet, basename='profile-template')
router.register(r'sites/profile/(?P<profile_pk>\d+)/extra-profile-images', ExtraProfileImagesViewSet, basename='profile-extra-images')
router.register('sites/all_experiences', AllExperienceViewSet, basename='all-experience')
router.register(r'sites/experience/(?P<experience_pk>\d+)/whatdid', ExperienceWhatDidViewSet, basename='experience-whatdid')
router.register(r'sites/experience/(?P<experience_pk>\d+)/skillsandtools', ExperienceWhatDidViewSet, basename='experience-skills-and-tools')
router.register(r'sites/(?P<site_pk>\d+)/experiences', SiteExperienceViewSet, basename='site-experience')
router.register(r'sites/(?P<site_pk>\d+)/keyqualification', KeyQualificationViewSet, basename='site-key-qualification')
router.register(r'sites/(?P<site_pk>\d+)/personalizedemailsettings', PersonalizedEmailSettingViewSet, basename='site-prsonalized-email-settings')



router.register(r'cms/site/(?P<site_pk>\d+)/tags', CmsTagViewSet, basename='csm-site-tags')
router.register(r'cms/site/(?P<site_pk>\d+)/category', CmsCategoryViewSet, basename='csm-site-categories')
router.register(r'cms/site/(?P<site_pk>\d+)/blogs', CmsBlogViewSet, basename='csm-site-blogs')




router.register(r'content_type', ContentTypeViewSet, basename='content-types')
router.register(r'content_type/(?P<content_type_pk>\d+)/object/(?P<object_pk>\d+)/comments', ContentTypeCommentViewSet, basename='content-types-comments')









urlpatterns = [
    path('', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),    
    path('hdapi.json/', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    
    
    path('token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', DecoratedTokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', DecoratedTokenBlacklistView.as_view(), name='token_blacklist'),
    
    
    path('', include(router.urls)),
    
    # path('tags/', TagListCreateView.as_view(), name='tag_list_create'),
    # path('tags/<int:pk>/', TagRetrieveUpdateDestroyView.as_view(), name='tag_retrieve_update_destroy'),
    # path('tags/<int:pk>/count/', TagViewCount.as_view(), name='tag_view_count'),
    # path('tags/site/', TagSiteListView.as_view(), name='tag_site_list'),
    

]








