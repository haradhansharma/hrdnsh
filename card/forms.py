from django import forms
from django.forms import ModelForm
from .models import *

class ContactModelForm(ModelForm):    
    class Meta:
        model = Contacts
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class':'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your Email', 'class':'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class':'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message', 'class':'form-control'}),
        }
        
class ServiceInqueryModelForm(ModelForm):    
    class Meta:
        model = ServiceInquery
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
           
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class':'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your Email', 'class':'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class':'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message', 'class':'form-control'}),
        }

