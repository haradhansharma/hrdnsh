from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from cms.models import Blog, Category, Comment, Tag

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

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from rest_framework.permissions import DjangoObjectPermissions

from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from common.context_processor import get_extra_images
from common.models import Experience, ExtraProfileImages, KeyQualification, PersonalizedEmailSetting, SelectedTemplate, SiteProfile, SkillsAndTools, WhatDidThere
from hdapi.pagination import Pagination30
from hdapi.schema import schema_for_create
from hdapi.serializers import (
    AllExperienceSerializer,
    CmsBlogSerializer,
    CmsCategorySerializer,
    CmsTagSerializer,
    ContentTypeCommentSerializer,
    ContentTypeSerializer,
    ExtraProfileImagesSerializer,
    KeyQualificationSerializer,
    PersonalizedEmailSettingSerializer,
    SelectTemplateSerializer,
    SiteExperienceSerializer,
    SiteProfileSerializer,
    SiteSerializer,
    SkillsAndToolsSerializer,
    TokenBlacklistResponseSerializer, 
    TokenObtainPairResponseSerializer, 
    TokenRefreshResponseSerializer, 
    TokenVerifyResponseSerializer,
    WhatDidSerializer
)
from hdapi.viewsets import NonListModelViewSet
from django.contrib.contenttypes.models import ContentType 


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    

class SiteViewSet(NonListModelViewSet):
    queryset = Site.objects.select_related('profile').select_related('profile__selected_template').all()
    serializer_class = SiteSerializer
    permission_classes = [permissions.IsAuthenticated]  
    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    

class SiteProfileViewSet(NonListModelViewSet):
    serializer_class = SiteProfileSerializer
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]
    permission_classes = [permissions.IsAuthenticated]  
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        site_id = self.kwargs.get('pk')   
        if site_id:
            context['site'] = int(site_id)
        return context

    def get_queryset(self):
        site_id = self.kwargs.get('pk')    
        if site_id:
            return SiteProfile.objects.filter(site_id=int(site_id))
        return SiteProfile.objects.none() 
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
class ProfileTemplateViewSet(NonListModelViewSet):
    queryset = SelectedTemplate.objects.all()
    serializer_class = SelectTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]  
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        profile_id = self.kwargs.get('pk') 
        if profile_id:  
            context['profile'] = int(profile_id)
        return context
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class AllExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = AllExperienceSerializer
    permission_classes = [permissions.IsAuthenticated & DjangoObjectPermissions]   
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['responsibility_or_designation', 'experience_type']
        
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
class SiteExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = SiteExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FileUploadParser]

    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Experience.objects.filter(site_id=int(site_id))
        return Experience.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
class ExperienceWhatDidViewSet(viewsets.ModelViewSet):
    serializer_class = WhatDidSerializer
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [FileUploadParser]

    
    def get_queryset(self):   
        experience_id = self.kwargs.get('experience_pk') 
        if experience_id:
            return WhatDidThere.objects.filter(experience_id=int(experience_id))
        return WhatDidThere.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class ExperienceSkillsAndToolsViewSet(viewsets.ModelViewSet):
    serializer_class = SkillsAndToolsSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FileUploadParser]
    
    def get_queryset(self):   
        experience_id = self.kwargs.get('experience_pk') 
        if experience_id:
            return SkillsAndTools.objects.filter(experience_id=int(experience_id))
        return SkillsAndTools.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class KeyQualificationViewSet(viewsets.ModelViewSet):
    serializer_class = KeyQualificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [FileUploadParser]
    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return KeyQualification.objects.filter(site_id=int(site_id))
        return KeyQualification.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
class ExtraProfileImagesViewSet(viewsets.ModelViewSet):
    serializer_class = ExtraProfileImagesSerializer
    pagination_class = Pagination30
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FileUploadParser]
    
    def get_queryset(self):   
        profile_id = self.kwargs.get('profile_pk') 
        if profile_id:
            profile = SiteProfile.objects.get(pk=int(profile_id))
            get_extra_images(profile)
            return ExtraProfileImages.objects.filter(profile=profile)  
        return ExtraProfileImages.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
 
class PersonalizedEmailSettingViewSet(viewsets.ModelViewSet):
    serializer_class = PersonalizedEmailSettingSerializer
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [FileUploadParser]
    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return PersonalizedEmailSetting.objects.filter(site_id=int(site_id))
        return PersonalizedEmailSetting.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class CmsTagViewSet(viewsets.ModelViewSet):
    serializer_class = CmsTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [FileUploadParser]
    
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
    
class ContentTypeCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ContentTypeCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [FileUploadParser]
    
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
    
    
    @schema_for_create(serializer_class=serializer_class)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
    

class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [FileUploadParser]
    

class CmsCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CmsCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [FileUploadParser]
    
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
    
    
class CmsBlogViewSet(viewsets.ModelViewSet):
    serializer_class = CmsBlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FileUploadParser]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        site_id = self.kwargs.get('site_pk')    
        if site_id:
            context['site_id'] = int(site_id)
        return context
    
    def get_queryset(self):   
        site_id = self.kwargs.get('site_pk') 
        if site_id:
            return Blog.objects.filter(site_id=int(site_id))
        return Blog.objects.none()    
    
    @schema_for_create(serializer_class=serializer_class)
    def create(self, request, *args, **kwargs):       
        return super().create(request, *args, **kwargs)    
    
    def perform_create(self, serializer):
        site_id = self.kwargs.get('site_pk') 
        serializer.validated_data['site_id'] = int(site_id)      
        serializer.save()
        
        
  

    

    
    
    
