

from cms.models import Blog, Category, Tag
from common.models import Experience, KeyQualification, SkillsAndTools
from service.models import Service
from django.core.cache import cache


def get_experience(request):
    c_experiences = cache.get(f"experiences{request.site.id}")
    if c_experiences is not None:
        return c_experiences
    experiences = Experience.on_site.all().order_by('-id')  
    cache.set(f"experiences{request.site.id}", experiences)
    return experiences

def get_qualifications(request):
    c_qualifications = cache.get(f"qualifications{request.site.id}")
    if c_qualifications is not None:
        return c_qualifications
    qualifications = KeyQualification.on_site.all()  
    cache.set(f"qualifications{request.site.id}", qualifications)
    return qualifications

def get_services(request):
    c_services = cache.get(f"services{request.site.id}")
    if c_services is not None:
        return c_services
    services = Service.status_objects.published_on_site(request).order_by('-created_at')
    cache.set(f"services{request.site.id}", services)
    return services

def get_skills(request):
    c_skills = cache.get(f"skills{request.site.id}")
    if c_skills is not None:
        return c_skills
    skills = SkillsAndTools.on_site.all()  
    cache.set(f"skills{request.site.id}", skills)
    return skills

def get_categories(request):
    
    c_categories = cache.get(f"categories{request.site.id}")
    if c_categories is not None:
        return c_categories   
    categories = Category.on_site.all()    
    cache.set(f"categories{request.site.id}", categories)    
    
    return categories


def get_popular_tags(request):
    c_popular_tags = cache.get(f"popular_tags{request.site.id}")
    if c_popular_tags is not None:
        return c_popular_tags  
            
    tags = Tag.on_site.prefetch_related('blog_related', 'view')         
    tag_data = {}   
    for tag in tags:
        try:             
            tag_view_count = tag.view.get().count                
            blog_count = tag.blog_related.count()        
            score = tag_view_count * 0.5 + blog_count * 0.5
            tag_data[tag] = score
        except Exception as e:        
            pass

    # Sort tags by view count and blog count
    popular_tags = sorted(tag_data.items(), key=lambda x: x[1], reverse=True)[:10]
    
    cache.set(f"popular_tags{request.site.id}", popular_tags)
    
    return popular_tags

def get_public_blogs(request):
    c_public_blogs = cache.get(f"public_blogs{request.site.id}")
    if c_public_blogs is not None:
        return c_public_blogs
    blogs = Blog.status_objects.published_on_site(request)     
    cache.set(f"public_blogs{request.site.id}", blogs)
    return blogs

    