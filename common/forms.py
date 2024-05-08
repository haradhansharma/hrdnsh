

from django import forms
from common.models import PersonalizedEmailSetting


class PersonalizedEmailSettingsForm(forms.ModelForm):
    class Meta:
        model = PersonalizedEmailSetting
        fields = '__all__'
        widgets = {            
            'host_password': forms.PasswordInput(),
        }
        