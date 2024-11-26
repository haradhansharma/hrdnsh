from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from contact.utils import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.templatetags.static import static
from common.context_processor import site_profile
from .forms import ContactForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
import logging
log =  logging.getLogger('log')


class HomeView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:success')
    
    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response['X-Robots-Tag'] = 'INDEX, FOLLOW'
        return response
    
    def get_profile(self):
        return site_profile(self.request)

    def form_valid(self, form):
        obj = form.save(commit = False)        
        obj.site = self.request.site
        obj.save()
        
        profile = self.get_profile()
        personal_settings = self.request.site.personalized_setting if hasattr(self.request.site, 'personalized_setting') else None
        
        if personal_settings is None:
            messages.warning(self.request, f'Message not sent, there is error! Please sent your email to {profile_email}')
            return
            
        
        
        form_email = form.cleaned_data['email']
        # Send email to user
        user_subject = f'{profile.get("profile_name")}-Thank you for contacting me!'
        user_html_message = render_to_string(
            'emails/user_contact_email.html', 
            {
                'name': form.cleaned_data['name'], 
                'profile_name' : profile.get('profile_name'), 
                'personal_settings' : personal_settings
            })
        user_plain_message = strip_tags(user_html_message)
        
        profile_email = personal_settings.email if personal_settings else profile.get('email')
        profile_domain = profile.get('domain')
        
        try:
            send_mail(
                user_subject, 
                user_plain_message, 
                personal_settings.email if personal_settings else settings.DEFAULT_FROM_EMAIL, 
                [form_email], 
                auth_user=personal_settings.host_user if personal_settings else settings.EMAIL_HOST_USER, 
                auth_password=personal_settings.host_password if personal_settings else settings.EMAIL_HOST_PASSWORD, 
                html_message=user_html_message
            )
        except Exception as e:
            messages.warning(self.request, f'Message not sent there is error! Please sent your email to {profile_email}')
            log.warning(f'WARNING: Contact email not sent for profile {profile_domain} DUE TO: {e} ')
            
            return HttpResponseRedirect(self.request.path)

        # Send email to profile
        admin_subject = f'{profile.get("profile_name")}-New contact submitted'
        admin_html_message = render_to_string(
            'emails/admin_email.html', 
            {
                'name': form.cleaned_data['name'], 
                'email': form_email, 
                'message': form.cleaned_data['message'], 
                'profile_name' : profile.get('profile_name')
            }
        )
        admin_plain_message = strip_tags(admin_html_message)
        try:
            send_mail(
                admin_subject, 
                admin_plain_message, 
                settings.EMAIL_HOST_USER, 
                [personal_settings.email if personal_settings else profile.get('email')], 
                reply_to = [form_email],
                html_message=admin_html_message
            )
        except Exception as e:            
            log.warning(f'WARNING: Contact form notification not sent to profile {profile_domain} DUE TO: {e} ')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        profile = self.get_profile()
        profile['meta_title'] = profile.get('contact_page_title')
        profile['meta_description'] = profile.get('contact_page_description')[:140] + ' ...' if len(profile.get('contact_page_description')) > 140 else profile.get('contact_page_description')
     
        profile['meta_image'] = self.request.build_absolute_uri(profile.get('contact_page_picture'))
        context['profile'] = profile        
     
        return context
    
def success_view(request):
    return render(request, 'contact/success.html')
  