from django.contrib import admin
from .models import *

admin.site.register(SiteProfile)
admin.site.register(KeyQualification)
admin.site.register(SiteTemplate)


class WhatDidThereInline(admin.TabularInline): 
    model = WhatDidThere
    extra = 1  
    
class SkillsAndToolsInline(admin.TabularInline): 
    model = SkillsAndTools
    extra = 1  

class ExperienceAdmin(admin.ModelAdmin):
    inlines = [WhatDidThereInline, SkillsAndToolsInline]

admin.site.register(Experience, ExperienceAdmin)
