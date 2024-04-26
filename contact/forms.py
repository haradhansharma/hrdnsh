from django import forms
from .models import Contact
from django_recaptcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from django_recaptcha.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'captcha':
                field.widget.attrs['class'] = 'form-control form-control-lg'
                field.widget.attrs['placeholder'] = field_name.capitalize()
                field.widget.attrs['rows'] = 5
                
            

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        
        