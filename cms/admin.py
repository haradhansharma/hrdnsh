from django import forms
from django_select2 import forms as s2forms
from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class BlogAdminForm(forms.ModelForm): 
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'tags': s2forms.Select2TagWidget(attrs={'data-placeholder': 'Select or create tags'}),
            'category': forms.Select(attrs={'data-placeholder': 'Select or create tags'}),
        }
        
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('body', )
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status',)

    form = BlogAdminForm
    
    class Media:
        css = {
            'all': ('assets/css/custom_admin.css',)
        }

admin.site.register(Blog, BlogAdmin)

class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('body', )
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status',)
    
    class Media:
        css = {
            'all': ('assets/css/custom_admin.css',)
        }

admin.site.register(Page, PageAdmin)



admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)


