from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account.models import User

class PercomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

class PercomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)