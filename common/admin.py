from django.contrib import admin
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
admin.site.register(Site)


class WhatDidThereInline(admin.TabularInline): 
    model = WhatDidThere
    extra = 1  
    
class SkillsAndToolsInline(admin.TabularInline): 
    model = SkillsAndTools
    extra = 1  
    

    


class ExperienceAdmin(admin.ModelAdmin):
    inlines = [WhatDidThereInline, SkillsAndToolsInline]

admin.site.register(Experience, ExperienceAdmin)
