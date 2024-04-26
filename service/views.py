from django.http import HttpResponse
from django.shortcuts import render
from cms.models import Like, View
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from common.context_processor import site_profile
from common.views import get_qualifications
from service.models import Service
from django.utils.html import strip_tags
from django.views.decorators.clickjacking import xframe_options_exempt  
from django.utils.decorators import method_decorator
from django.contrib.contenttypes.models import ContentType

# Create your views here.
class ServiceHomeView(ListView):
    model = Service
    template_name = 'service/services.html'
    paginate_by = 5
    
    def get_queryset(self):      
        queryset = self.model.status_objects.published_on_site(self.request).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
      
        profile = site_profile(self.request)   
        profile['meta_title'] = profile.get('service_page_title')
        profile['meta_description'] = profile.get('service_page_description')[:136] + ' ...' if len(profile.get('service_page_description')) > 140 else profile.get('service_page_description')
        service_page_picture = profile.get('service_page_picture')
        profile['meta_image'] = self.request.build_absolute_uri(service_page_picture.url)
        
        context['profile'] = profile
        
        return context
    


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service/service_details.html'
    context_object_name = 'service'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        obj = self.get_object()        
        
        qualifications = get_qualifications()   
        context['qualifications'] = qualifications                
        
        obj.increment_view_count()          
        
        view = obj.view.get()  

        context['view_count'] = view.count        
        
        profile = site_profile(self.request)   
        profile['meta_title'] = obj.title
        sumamry = strip_tags(obj.summary)
        profile['meta_description'] = sumamry[:136] + ' ...' if len(sumamry) > 140 else sumamry
        obj_picture = obj.main_image
        profile['meta_image'] = self.request.build_absolute_uri(obj_picture.url)        
        context['profile'] = profile
        
        
        return context