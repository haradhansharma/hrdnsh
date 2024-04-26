from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.templatetags.static import static
from common.context_processor import site_profile
from .forms import ContactForm
from django.contrib.sites.shortcuts import get_current_site

class HomeView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:success')
    
    def get_profile(self):
        return site_profile(self.request)

    def form_valid(self, form):
        obj = form.save(commit = False)        
        obj.site = get_current_site(self.request)
        obj.save()
        
        profile = self.get_profile()

        # Send email to user
        user_subject = 'Haradhan Sharma-Thank you for contacting me!'
        user_html_message = render_to_string('emails/user_contact_email.html', {'name': form.cleaned_data['name'], 'profile_name' : profile.get('profile_name')})
        user_plain_message = strip_tags(user_html_message)
        send_mail(
            user_subject, 
            user_plain_message, 
            settings.EMAIL_HOST_USER, 
            [form.cleaned_data['email']], 
            html_message=user_html_message
        )

        # Send email to admin
        admin_subject = 'Haradhan Sharma-New contact submitted'
        admin_html_message = render_to_string(
            'emails/admin_email.html', 
            {
                'name': form.cleaned_data['name'], 
                'email': form.cleaned_data['email'], 
                'message': form.cleaned_data['message'], 
                'profile_name' : profile.get('profile_name')
            }
        )
        admin_plain_message = strip_tags(admin_html_message)
        send_mail(
            admin_subject, 
            admin_plain_message, 
            settings.EMAIL_HOST_USER, 
            [settings.ADMIN_EMAIL], 
            html_message=admin_html_message
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        profile = self.get_profile()
        profile['meta_title'] = profile.get('contact_page_title')
        profile['meta_description'] = profile.get('contact_page_description')[:136] + ' ...' if len(profile.get('contact_page_description')) > 140 else profile.get('contact_page_description')
        contact_page_picture = profile.get('contact_page_picture')
        profile['meta_image'] = self.request.build_absolute_uri(contact_page_picture.url)
        context['profile'] = profile        
     
        return context
    
def success_view(request):
    return render(request, 'contact/success.html')
  