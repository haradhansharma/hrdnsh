from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
 
    
)

from account.forms import (
    PercomUserCreationForm as UserCreationForm,
    PercomUserChangeForm as UserChangeForm
    )
from django.urls import reverse_lazy
from django.views import generic

class UserLoginView(LoginView):
    template_name = 'account/login.html'
    
class UserLogoutView(LogoutView):
    template_name = 'account/logged_out.html'
    

    
class UserSignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('account:dashboard')
    template_name = 'account/signup.html'
    

    
class UserPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change_form.html'
    success_url = reverse_lazy('account:password_change_done')
    
class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'
    
class UserPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.txt'
    success_url = reverse_lazy('account:password_reset_done')
    
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
    
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')
    
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'