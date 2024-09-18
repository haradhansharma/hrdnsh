from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from cms.models import Blog, Category, Comment, Page, Tag

from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from rest_framework import viewsets, permissions, filters

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.exceptions import MethodNotAllowed

from rest_framework.parsers import MultiPartParser, JSONParser, FileUploadParser, FormParser

from rest_framework.permissions import DjangoObjectPermissions

from drf_yasg import openapi

from django_filters.rest_framework import DjangoFilterBackend   
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from common.context_processor import get_extra_images
from common.models import (
    Experience, 
    ExtraProfileImages, 
    KeyQualification, 
    PersonalizedEmailSetting, 
    SelectedTemplate, 
    SiteProfile, 
    SkillsAndTools, 
    WhatDidThere
    )
from hdapi.filters import BlogFilter
from hdapi.pagination import Pagination30
from hdapi.permissions import IsAssociatedSiteOwnerOrProfileOwner
from hdapi.schema import schema_for_create, schema_for_destroy, schema_for_retrieve, schema_for_update
from hdapi.serializers import ( 
    CmsBlogSerializer,
    CmsCategorySerializer,
    CmsPageSerializer,
    CmsTagSerializer,
    ContentTypeCommentSerializer,
    ContentTypeSerializer,
    ExtraProfileImagesSerializer,
    GroupSerializer,
    KeyQualificationSerializer,
    PersonalizedEmailSettingSerializer,
    ProjectRequirementSerializer,
    ProjectScoopeSerializer,
    ProjectSerializer,
    ScoopVisualizationSerializer,
    SelectTemplateSerializer,
    ServiceSerializer,
    SiteExperienceSerializer,
    SiteProfileSerializer,
    SiteSerializer,
    SkillsAndToolsSerializer,
    TokenBlacklistResponseSerializer, 
    TokenObtainPairResponseSerializer, 
    TokenRefreshResponseSerializer, 
    TokenVerifyResponseSerializer,
    UserSerializer,
    WhatDidSerializer
)
from hdapi.viewsets import(
    NonListModelViewSet, 
    RetriveUpdateDeleteModelViewSet,
    RetriveUpdateModelViewSet
    )
from django.contrib.contenttypes.models import ContentType

from project.models import Project, ProjectRequirement, ProjectScoope, ScoopVisualization
from service.models import Service 
from django.contrib.auth.models import Group

class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        },
        security=[{"Basic": []}] 
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        },
        security=[{"Bearer": []}] 
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        },
        security=[{"Bearer": []}] 
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class DecoratedTokenBlacklistView(TokenBlacklistView):
    permission_classes = [permissions.IsAdminUser]  

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        },
        security=[{"Bearer": []}] 
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.select_related(
        'profile').select_related(
            'profile__selected_template').select_related(
                'personalized_setting').all()
    serializer_class = SiteSerializer    
    permission_classes = [permissions.IsAdminUser]
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)  
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        site = serializer.save()
        profile = SiteProfile.objects.create(site=site)
        SelectedTemplate.objects.create(profile=profile)
        PersonalizedEmailSetting.objects.create(site=site)
    
    

class SiteProfileViewSet(RetriveUpdateModelViewSet):
    serializer_class = SiteProfileSerializer  
    parser_classes = [MultiPartParser, JSONParser] # Must update commit of drf-yasg consumes utils.py >> get_consumes
    
    def get_queryset(self):
        site_id = self.kwargs.get('pk')    
        print(site_id)
        if site_id:
            return SiteProfile.objects.filter(site_id=int(site_id))
        return SiteProfile.objects.none() 
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)  
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs) 
      
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)   
    
    
class ProfileTemplateViewSet(RetriveUpdateModelViewSet):
    queryset = SelectedTemplate.objects.all()
    serializer_class = SelectTemplateSerializer
   
    
    def get_queryset(self):   
        profile_id = self.kwargs.get('profile_pk')    
        if profile_id:
            return SelectedTemplate.objects.filter(profile_id=int(profile_id))
        return SelectedTemplate.objects.none()  
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)  
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs) 
      
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    
class PersonalizedEmailSettingViewSet(RetriveUpdateModelViewSet):
    serializer_class = PersonalizedEmailSettingSerializer

    
    def get_queryset(self):   
        site_id = self.kwargs.get('pk') 
        if site_id:
            return PersonalizedEmailSetting.objects.filter(site_id=int(site_id))
        return PersonalizedEmailSetting.objects.none() 
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs) 
      
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
class ExtraProfileImagesViewSet(viewsets.ModelViewSet):
    serializer_class = ExtraProfileImagesSerializer
    pagination_class = Pagination30
    parser_classes = [MultiPartParser, JSONParser] # Must update commit of drf-yasg consumes utils.py >> get_consumes
    
    def get_queryset(self):   
        profile_id = self.kwargs.get('profile_pk')       
        if profile_id:
            profile = SiteProfile.objects.get(pk=int(profile_id))
            get_extra_images(profile)
            return ExtraProfileImages.objects.filter(profile_id=int(profile_id))  
        return ExtraProfileImages.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.validated_data ['profile_id'] = int(self.kwargs.get('profile_pk'))
        serializer.save()
    
    
class SiteExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = SiteExperienceSerializer
    
    def get_queryset(self):        
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Experience.objects.filter(site_id=int(site_id))
        return Experience.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.validated_data ['site_id'] = int(self.kwargs.get('site_pk'))
        serializer.save()
    
    
class ExperienceWhatDidViewSet(viewsets.ModelViewSet):
    serializer_class = WhatDidSerializer
        
    def get_queryset(self):        
        experience_id = self.kwargs.get('experience_pk') 
        if experience_id:
            return WhatDidThere.objects.filter(experience_id=int(experience_id))
        return WhatDidThere.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.validated_data ['experience_id'] = int(self.kwargs.get('experience_pk'))
        serializer.save()
    
class ExperienceSkillsAndToolsViewSet(viewsets.ModelViewSet):
    serializer_class = SkillsAndToolsSerializer
    parser_classes = [MultiPartParser, JSONParser] # Must update commit of drf-yasg consumes utils.py >> get_consumes

    
    def get_queryset(self):   
        experience_id = self.kwargs.get('experience_pk') 
        if experience_id:
            return SkillsAndTools.objects.filter(experience_id=int(experience_id))
        return SkillsAndTools.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.validated_data ['experience_id'] = int(self.kwargs.get('experience_pk'))
        serializer.save()
    

class KeyQualificationViewSet(viewsets.ModelViewSet):
    serializer_class = KeyQualificationSerializer
  
    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return KeyQualification.objects.filter(site_id=int(site_id))
        return KeyQualification.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.validated_data ['site_id'] = int(self.kwargs.get('site_pk'))
        serializer.save() 

    
class CmsTagViewSet(viewsets.ModelViewSet):
    serializer_class = CmsTagSerializer

    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        site_id = self.kwargs.get('site_pk')    
        if site_id:
            context['site_id'] = int(site_id)
        return context
    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Tag.objects.filter(site_id=int(site_id))
        return Tag.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class ContentTypeCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentTypeCommentSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        content_type_id = self.kwargs.get('content_type_pk')  
        object_id = self.kwargs.get('object_pk')   
         
        if content_type_id:
            context['content_type_id'] = int(content_type_id)
            context['object_id'] = int(object_id)
            
        return context
    
    def get_queryset(self):   
        content_type_id = self.kwargs.get('content_type_pk') 
        if content_type_id:
            return Comment.objects.filter(content_type_id=int(content_type_id))
        return Comment.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
    @schema_for_create(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)    
    

class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    

class CmsCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CmsCategorySerializer

    
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        site_id = self.kwargs.get('site_pk')    
        if site_id:
            context['site_id'] = int(site_id)
        return context
    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Category.objects.filter(site_id=int(site_id))
        return Category.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    

class CmsBlogViewSet(viewsets.ModelViewSet):
    serializer_class = CmsBlogSerializer
    parser_classes = [MultiPartParser, JSONParser] # Must update commit of drf-yasg consumes utils.py >> get_consumes

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = BlogFilter
    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Blog.objects.filter(site_id=int(site_id))
        return Blog.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
    def perform_create(self, serializer):
        site_id = self.kwargs.get('site_pk') 
        serializer.validated_data['site_id'] = int(site_id)      
        serializer.save()
        
        
class CmsPageViewSet(viewsets.ModelViewSet):
    serializer_class = CmsPageSerializer
    parser_classes = [MultiPartParser, JSONParser]
    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Page.objects.filter(site_id=int(site_id))
        return Page.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
    def perform_create(self, serializer):
        site_id = self.kwargs.get('site_pk') 
        serializer.validated_data['site_id'] = int(site_id)      
        serializer.save()
        
        
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    parser_classes = [MultiPartParser, JSONParser] # Must update commit of drf-yasg consumes utils.py >> get_consumes

    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Project.objects.filter(site_id=int(site_id))
        return Project.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
    def perform_create(self, serializer):
        site_id = self.kwargs.get('site_pk') 
        serializer.validated_data['site_id'] = int(site_id)      
        serializer.save()
        
        
class ProjectRequirementViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectRequirementSerializer
    
    def get_queryset(self):   
        project_id = self.kwargs.get('project_pk')        
        if project_id :
            return ProjectRequirement.objects.filter(project_id=int(project_id))
        return ProjectRequirement.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk') 
        serializer.validated_data['project_id'] = int(project_id)      
        serializer.save()  
    
class ProjectScoopeViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectScoopeSerializer
    
    
    def get_queryset(self):   
        project_id = self.kwargs.get('project_pk')         
        if project_id:
            return ProjectScoope.objects.filter(
                project_id=int(project_id)
                )
        return ProjectScoope.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs) 
    
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk') 
        serializer.validated_data['project_id'] = int(project_id)      
        serializer.save()  
    
    
class ScoopVisualizationViewSet(viewsets.ModelViewSet):
    serializer_class = ScoopVisualizationSerializer
    parser_classes = [MultiPartParser, JSONParser] # Must update commit of drf-yasg consumes utils.py >> get_consumes

    
    def get_queryset(self):   
        scoope_id = self.kwargs.get('scoope_pk')    
        if scoope_id:
            return ScoopVisualization.objects.filter(
                project_scoope_id = int(scoope_id))
        return ScoopVisualization.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        scoope_id = self.kwargs.get('scoope_pk') 
        serializer.validated_data['project_scoope_id'] = int(scoope_id)      
        serializer.save()     
        
        
class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    parser_classes = [MultiPartParser, JSONParser] # Must update commit of drf-yasg consumes utils.py >> get_consumes

    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Service.objects.filter(site_id=int(site_id))
        return Service.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @schema_for_retrieve(serializer_class=serializer_class)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @schema_for_update(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)   
    
    @schema_for_update(serializer_class=serializer_class)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs) 
    
    @schema_for_destroy(serializer_class=serializer_class)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)  
    
    def perform_create(self, serializer):
        site_id = self.kwargs.get('site_pk') 
        serializer.validated_data['site_id'] = int(site_id)      
        serializer.save()
    

        
        
  

    

    
    
    
