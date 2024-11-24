from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from service.models import Service
from django import forms
from django_select2 import forms as s2forms

class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'skills': s2forms.Select2TagWidget(attrs={'data-placeholder': 'Select or create Skills'}),          
        }


class ServiceAdmin(SummernoteModelAdmin):
    summernote_fields = ('body', 'summary', )
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status',)
    
    fields = [
        "title", 
        "slug", 
        "buy_link",
        "main_image",          
        "summary", 
        "body",
        "skills",
        "category",
        "site",
        "status",
        
        
        ]
    
    # form = ServiceAdminForm
    
    


    
    class Media:
        css = {
            'all': ('assets/css/custom_admin.css',)
        }

admin.site.register(Service, ServiceAdmin)
