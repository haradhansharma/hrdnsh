from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from django.contrib.sites.models import Site
from account.models import User
from cms.models import Blog, Category, Comment, Tag, View
from django.contrib.contenttypes.models import ContentType
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
from project.models import Project, ProjectRequirement, ProjectScoope, ScoopVisualization
from service.models import Service
from django.contrib.auth.models import Group

class HdTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)   
   
        token['email'] = user.email
   

        return token
    
    
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
    
class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
    
class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
    
class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()
    def update(self, instance, validated_data):
        raise NotImplementedError()    
    
'''
===================
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'    


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        

        



class ViewSerializer(serializers.ModelSerializer):        
    class Meta:
        model = View
        fields = ['count', 'last_viewed']
        
class ContentTypeCommentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    
    def create(self, validated_data):
        content_type_id = self.context['content_type_id']
        object_id = self.context['object_id']        
        return Comment.objects.create(content_type_id=content_type_id, object_id=object_id, **validated_data)
    
    class Meta:
        model = Comment
        fields = ['id', 'body', 'site', 'email'] 
        
       
class ServiceSerializer(serializers.ModelSerializer): 
    view = ViewSerializer(many=True, read_only=True)  
    absolute_url = serializers.SerializerMethodField()  
    
    class Meta:
        model = Service    
        fields = '__all__'
        read_only_fields = ('site', 'slug',)  
    
    
    def get_absolute_url(self, service: Service):
        return f'https://{service.site.domain}{service.get_absolute_url()}' 
        
        
class ScoopVisualizationSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ScoopVisualization    
        fields = '__all__'   
        read_only_fields = ('project_scoope',)      
        
class ProjectScoopeSerializer(serializers.ModelSerializer): 
    scoope_visualization = ScoopVisualizationSerializer(many=True, read_only=True)
    class Meta:
        model = ProjectScoope    
        fields = '__all__'  
        read_only_fields = ('project',)            

class ProjectRequirementSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ProjectRequirement    
        fields = '__all__'  
        read_only_fields = ('project',)   
        
        
class ProjectSerializer(serializers.ModelSerializer): 
    view = ViewSerializer(many=True, read_only=True)  
    absolute_url = serializers.SerializerMethodField()  
    project_requirements = ProjectRequirementSerializer(many=True, read_only=True)
    project_scoopes = ProjectScoopeSerializer(many=True, read_only=True)    
    
    class Meta:
        model = Project    
        fields = '__all__'
        read_only_fields = ('site', 'slug',)  
    
    
    def get_absolute_url(self, project: Project):
        return f'https://{project.site.domain}{project.get_absolute_url()}' 
        
        
class CmsBlogSerializer(serializers.ModelSerializer):
    view = ViewSerializer(many=True, read_only=True)
    comments = ContentTypeCommentSerializer(many=True, read_only=True)
    content_type_id = serializers.SerializerMethodField(method_name='get_cached_content_type_id', read_only=True)
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Blog    
        exclude = ()
        read_only_fields = ('site', 'slug', )
        
    def get_cached_content_type_id(self, blog: Blog):
        if hasattr(blog, 'cached_content_type_id'):
            return blog.cached_content_type_id

        content_type = ContentType.objects.get_for_model(blog)
        blog.cached_content_type_id = content_type.id
        return content_type.id
    
    def get_absolute_url(self, blog: Blog):
        return f'https://{blog.site.domain}{blog.get_absolute_url()}' 


        
class CmsCategorySerializer(serializers.ModelSerializer):
    view_blogs_on_site = serializers.SerializerMethodField(method_name='process_abs_url', help_text="Will return url to view blogs of this category on the site!")
    view_projects_on_site = serializers.SerializerMethodField( help_text="Will return url to view projects of this category on the site!")
    view_service_on_site = serializers.SerializerMethodField(help_text = "Will return url to view services of this category on the site!")
 
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title', 'body', 'view_blogs_on_site', 'view_projects_on_site', 'view_service_on_site'] 
        read_only_fields = ('slug',)
    def process_abs_url(self, category: Category):
        return f'https://{category.site.domain}{category.get_absolute_url()}'
    
    def get_view_projects_on_site(self, category: Category):
        return f'https://{category.site.domain}{category.get_projectcat_absolute_url()}'
      
    def get_view_service_on_site(self, category: Category):
        return f'https://{category.site.domain}{category.get_servicecat_absolute_url()}'
          
        
    def create(self, validated_data):      
        site_id = self.context['site_id']        
        return Category.objects.create(site_id=site_id, **validated_data) 

class ContentTypeSerializer(serializers.ModelSerializer):        
    class Meta:
        model = ContentType
        fields = '__all__'        

class CmsTagSerializer(serializers.ModelSerializer):
    get_tag_blogs_url = serializers.SerializerMethodField(method_name='process_get_tag_blogs_url', help_text="Will return url to view blogs of this tag on the site!")
    view = ViewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'get_tag_blogs_url', 'view'] 
        
        
    def process_get_tag_blogs_url(self, tag: Tag):
        return f'https://{tag.site.domain}{tag.get_tag_blogs_url()}'    
 
        
    def create(self, validated_data):      
        site_id = self.context['site_id']        
        return Tag.objects.create(site_id=site_id, **validated_data) 
        
        
class KeyQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyQualification
        fields = '__all__'  
        read_only_fields = ('site',)   
        
        
class SkillsAndToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillsAndTools
        fields = '__all__'   
        read_only_fields = ('experience',)    
        
class WhatDidSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatDidThere
        fields = '__all__'  
        read_only_fields = ('experience',)          
   
        

class SiteExperienceSerializer(serializers.ModelSerializer):
    skills_to_site = SkillsAndToolsSerializer(many=True, read_only=True)
    what_did = WhatDidSerializer(many=True, read_only=True)
    class Meta:
        model = Experience
        fields = '__all__'  
        read_only_fields = ('site',)  
        

class ExtraProfileImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraProfileImages
        fields = '__all__'   
        read_only_fields = ('profile',)   
        
        
class PersonalizedEmailSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalizedEmailSetting
        fields = '__all__'   
        read_only_fields = ('site',)
        
        
class SelectTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedTemplate
        fields = '__all__'
        read_only_fields = ('profile',)
        
class SiteProfileSerializer(serializers.ModelSerializer):
    selected_template = SelectTemplateSerializer(read_only=True)
    class Meta:
        model = SiteProfile
        fields = '__all__' 
        read_only_fields = ('site',)
        

class SiteSerializer(serializers.ModelSerializer):  
    profile = SiteProfileSerializer(read_only=True)
    personalized_setting = PersonalizedEmailSettingSerializer(read_only=True)
    class Meta:
        model = Site
        fields = '__all__'
        

        
        
    
    
   