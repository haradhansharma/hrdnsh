from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):  
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['email'].widget = forms.HiddenInput()
              
    class Meta:
        model = Comment
        fields = ("body", "email")
        
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control form-control-sm rounded-5', 'rows': 5, 'placeholder': 'Enter reactions in your mind about the senses'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm rounded-5', 'placeholder': 'Enter Email'}),
            
        }


class CommentEditForm(forms.ModelForm):     
    class Meta:
        model = Comment
        fields = ("body",)
        
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control form-control-sm rounded-5', 'rows': 5, 'placeholder': 'Enter reactions in your mind about the senses'}),
            
        }