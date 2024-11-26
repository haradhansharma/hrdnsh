from django.contrib import admin

from common.forms import PersonalizedEmailSettingsForm
from .models import *
from django.contrib.sites.models import Site
from django_summernote.admin import SummernoteModelAdmin


class SelectedtemplateInline(admin.StackedInline): 
    model = SelectedTemplate
    extra = 1  
    
class ExtraImagesInline(admin.TabularInline):
    model = ExtraProfileImages
    extra = 1
    
class SiteProfileAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
   
        super().save_model(request, obj, form, change)        
  
        cache_key = f"site_profile{request.site.id}"  
        cache.delete(cache_key)
   
        self.message_user(request, f"Cache key '{cache_key}' deleted successfully. It will rebuild autometically based on updated information", level="info")

    
    inlines = [SelectedtemplateInline, ExtraImagesInline]
admin.site.register(SiteProfile, SiteProfileAdmin)


admin.site.register(KeyQualification)




class TemplateAdmin(SummernoteModelAdmin):
    summernote_fields = ('body', )
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status',)    
    class Media:
        css = {
            'all': ('assets/css/custom_admin.css',)
        }
admin.site.register(Template, TemplateAdmin)

admin.site.unregister(Site)
class PersonalizedEmailSettings(admin.StackedInline):
    model = PersonalizedEmailSetting
    extra = 1
    
    
class SiteAdmin(admin.ModelAdmin):
    inlines = [PersonalizedEmailSettings]
admin.site.register(Site, SiteAdmin)


class WhatDidThereInline(admin.TabularInline): 
    model = WhatDidThere
    extra = 1  
    
class SkillsAndToolsInline(admin.TabularInline): 
    model = SkillsAndTools
    extra = 1  
    

    


class ExperienceAdmin(admin.ModelAdmin):
    inlines = [WhatDidThereInline, SkillsAndToolsInline]

admin.site.register(Experience, ExperienceAdmin)






