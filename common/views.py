from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.templatetags.static import static
from common.caching import get_experience, get_qualifications, get_services, get_skills
from common.context_processor import site_profile
from service.models import Service
from .models import *


    

# Create your views here.
class HomeView(View):
    template_class = 'common/index.html'
    
    def get(self, request, *args, **kwargs):
        
        experiences = get_experience(request)     
        
        context = {
            'experiences' : experiences 
        }
        
        response = render(request, self.template_class, context)
        response['X-Robots-Tag'] = 'INDEX, FOLLOW'
        return response
        

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
    
    
    
class AboutView(View):
    template_class = 'common/about.html'
    
    def get(self, request, *args, **kwargs):
        experiences = get_experience(request) 
        qualifications = get_qualifications(request)   
        services = get_services(request) 
        skills = get_skills(request)  
        
        profile = site_profile(request)     
        
        profile['meta_title'] = f"About {profile.get('profile_name')}"
        profile['meta_description'] = profile.get('career_summary')[:140] + ' ...' if len(profile.get('career_summary')) > 140 else profile.get('career_summary')
    
        profile['meta_image'] = self.request.build_absolute_uri(profile.get('about_picture'))
      
        
        context = {
            'experiences' : experiences,
            'qualifications' : qualifications,
            'services' : services,
            'skills' : skills,
            'profile' : profile
        }
        
        
  
        response = render(request, self.template_class, context)
        response['X-Robots-Tag'] = 'INDEX, FOLLOW'
        return response
    
    
    
def webmanifest(request):
    profile = site_profile(request)     
    icons = []    
    ic128 = {
        "src": request.build_absolute_uri(profile.get('extra_images').get('icon128')),
        "sizes": "128x128",
        "type": "image/png",
        "purpose":"any maskable"        
    }
    
    icons.append(ic128)   
    ic256 = {
        "src": request.build_absolute_uri(profile.get('extra_images').get('icon256')),
        "sizes": "256x256",
        "type": "image/png",
        "purpose":"any maskable"        
    }
    
    icons.append(ic256)   
    ic512 = {
        "src": request.build_absolute_uri(profile.get('extra_images').get('icon512')),
        "sizes": "512x512",
        "type": "image/png",
        "purpose":"any maskable"        
    }
    icons.append(ic512)    
    data = {
        'name' : profile.get('profile_name'),
        'short_name' : profile.get('profile_name'),
        'icons' : icons,        
        "theme_color": "#a6034f",
        "background_color": "#a6034f",
        "display": "fullscreen",
        "start_url": profile.get('home_url'),        
    }
    
    return JsonResponse(data, safe=False)


def maintanace_redirect(request):
    template_class = 'maintanace_redirect.html'
    
    context = {
        
    }
    response = render(request, template_class, context)
    response['X-Robots-Tag'] = 'NOINDEX, NOFOLLOW'
    return response
    


