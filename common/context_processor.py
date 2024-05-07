from common.models import SiteProfile
from .menus import *
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.templatetags.static import static
from django.core.cache import cache

def site_profile(request):
  
    data = cache.get(f"site_profile{request.site.id}")
    
    if data is not None:
        return data
    
    
    current_site = get_current_site(request)
    try:
        current_site_profile = current_site.profile
    except:
        SiteProfile.objects.create(site=current_site)
        current_site_profile = current_site.profile


    data = {
        'domain' : current_site.domain,
        'site_name' : current_site.name,
        'meta_title' : current_site_profile.meta_title,
        'meta_description' : current_site_profile.meta_description,
        'visitor_addressing_first' : current_site_profile.visitor_addressing_first,
        'visitor_addressing_second' : current_site_profile.visitor_addressing_second,
        
        'profile_name' : current_site_profile.profile_name,
        'profile_title' : current_site_profile.profile_title,
        'email' : current_site_profile.email,
        'location' : current_site_profile.location,
        'location_geo_code' : current_site_profile.location_geo_code, 
        'phone' : current_site_profile.phone,
        'name_logo' : current_site_profile.name_logo.url if current_site_profile.name_logo else '',
        'name_logo_big' : current_site_profile.name_logo_big.url if current_site_profile.name_logo_big else '',
        'favicon' : current_site_profile.favicon.url if current_site_profile.favicon else '',
        'home_page_picture' : current_site_profile.home_page_picture.url if current_site_profile.home_page_picture else '',
        'about_picture' : current_site_profile.about_picture.url if current_site_profile.about_picture else '',
        'mask_icon' : current_site_profile.mask_icon.url if current_site_profile.mask_icon else '',
        'career_summary' : current_site_profile.career_summary,
        'education_header' : current_site_profile.education_header,
        'education_footer' : current_site_profile.education_footer,
        'blog_page_title' : current_site_profile.blog_page_title,
        'blog_page_description' : current_site_profile.blog_page_description,
        'blog_page_picture' : current_site_profile.blog_page_picture.url if current_site_profile.blog_page_picture else '',
        'project_page_title' : current_site_profile.project_page_title,
        'project_page_description' : current_site_profile.project_page_description,
        'project_page_picture' : current_site_profile.project_page_picture.url if current_site_profile.project_page_picture else '',
        'service_page_title' : current_site_profile.service_page_title,
        'service_page_description' : current_site_profile.service_page_description,
        'service_page_picture' : current_site_profile.service_page_picture.url if current_site_profile.service_page_picture else '',
        'contact_page_title' : current_site_profile.contact_page_title,
        'contact_page_description' : current_site_profile.contact_page_description,
        'contact_page_picture' : current_site_profile.contact_page_picture.url if current_site_profile.contact_page_picture else '',
        'youtube_intro_id' : current_site_profile.youtube_intro_id,
        
        'facebook_link' : current_site_profile.facebook_link,
        'twitter_link' : current_site_profile.twitter_link,
        'linkedin_link' : current_site_profile.linkedin_link,
        'instagram_link' : current_site_profile.instagram_link,
        'github_link' : current_site_profile.github_link,
        'upwork_link' : current_site_profile.upwork_link,
        'youtube_link' : current_site_profile.youtube_link,
        
        'years_of_experience' : current_site_profile.years_of_experience,
        'number_of_industries_works' : current_site_profile.number_of_industries_works,
        'number_of_clients' : current_site_profile.number_of_clients,
        
        'languages' : current_site_profile.languages.split(',') if current_site_profile.languages else [],
        'interest' : current_site_profile.interest.split(',') if current_site_profile.interest else [],
        
        
        
        'home_url' : request.build_absolute_uri(reverse('common:home')),
        'meta_image' : request.build_absolute_uri(current_site_profile.name_logo.url if current_site_profile.name_logo else '')
        
    }
    cache.set(f"site_profile{request.site.id}", data)
    return data

def common(request):
    
    context = {
        'mega_menu_items' : mega_menu_items(request),
        'profile' : site_profile(request)
    }
    
    return context