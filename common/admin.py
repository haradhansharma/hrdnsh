from django.contrib import admin
from .models import *
from django.contrib.sites.models import Site

class SelectedtemplateInline(admin.StackedInline): 
    model = SelectedTemplate
    extra = 1  
    
class SiteProfileAdmin(admin.ModelAdmin):
    inlines = [SelectedtemplateInline]
admin.site.register(SiteProfile, SiteProfileAdmin)


admin.site.register(KeyQualification)
admin.site.register(Template)

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
