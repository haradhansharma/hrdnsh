from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from common.context_processor import site_profile
from project.models import Project
from django.utils.html import strip_tags


# Create your views here.

class ProjectHomeView(ListView):
    model = Project
    template_name = 'project/projects.html'
    paginate_by = 5
    
    def get_queryset(self):      
        queryset = self.model.status_objects.published_on_site(self.request).order_by('-created_at')
        
        # Get the search query from the GET parameters
        search_query = self.request.GET.get('q')
        
        if search_query:
            # Filter the queryset based on title or content containing the search query
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(summary__icontains=search_query) | Q(project_requirements__item__icontains=search_query)).distinct()
        
        # Check if the 'slug' parameter exists in the URL kwargs
        if 'slug' in self.kwargs:
            # Filter the queryset based on the category slug
            queryset = queryset.filter(categories__slug=self.kwargs['slug'])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
      
        profile = site_profile(self.request)   
        profile['meta_title'] = profile.get('project_page_title')
        profile['meta_description'] = profile.get('project_page_description')[:136] + ' ...' if len(profile.get('project_page_description')) > 140 else profile.get('project_page_description')
    
        profile['meta_image'] = self.request.build_absolute_uri(profile.get('service_page_picture'))
        
        context['profile'] = profile
        
        return context
    

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_details.html'
    context_object_name = 'project'
    
    def get_queryset(self):      
        queryset = self.model.status_objects.published_on_site(self.request).order_by('-created_at')        
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        obj = self.get_object()    
        
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
        
        items = self.get_queryset().exclude(id=obj.id)[:6]        
           
        context['slide_list'] = self.create_slide_groups(items)   
            
        
        
        return context
    
    
    def create_slide_groups(self, items, slides_per_group=2):
        initial = 1
        slide_list = []
        slide_item = [] 
        
        for item in items:                       
            if len(slide_item) <= slides_per_group:    
                slide_item.append(item) 
            if len(slide_item) == slides_per_group:                
                slide_list.append({initial:slide_item})  
                slide_item = []
                initial += 1

        return slide_list
