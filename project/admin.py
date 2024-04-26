from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin, SummernoteInlineModelAdmin
from project.models import Project, ProjectRequirement, ProjectScoope, ScoopVisualization
from django import forms
from django_select2 import forms as s2forms

class ScoopVisualizationInline(admin.TabularInline): 
    model = ScoopVisualization
    extra = 1 
    show_change_link = True
    
class ProjectScoopeAdmin(SummernoteModelAdmin): 
    summernote_fields = ('scoope', 'outcome',)
    model = ProjectScoope 
    inlines = [ScoopVisualizationInline]
    
admin.site.register(ProjectScoope, ProjectScoopeAdmin)
    
    
class ProjectRequirementInline(admin.TabularInline): 
    model = ProjectRequirement
    extra = 1  

    
class ProjectScoopeInline(SummernoteInlineModelAdmin, admin.TabularInline): 
    summernote_fields = ('scoope', 'outcome',)
    model = ProjectScoope
    extra = 1    
    inlines = [ScoopVisualizationInline]
    

class ProjectAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status',)

    fields = [
        "title",
        "slug",
        "main_image",
        "summary",     
        "categories", 
        "site",            
        "author", 
        "status"   
        
        ]

    inlines = [ProjectRequirementInline, ProjectScoopeInline]
    class Media:
        css = {
            'all': ('assets/css/custom_admin.css',)
        }

admin.site.register(Project, ProjectAdmin)
