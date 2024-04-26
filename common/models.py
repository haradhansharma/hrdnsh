import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from cms.mixins import DateTimeMixin, SaveAndImageOptimizationMixin, SiteAutorMixin
from common.utils import optimize_image_for_web


class SiteProfile(SaveAndImageOptimizationMixin, models.Model):    
    site = models.OneToOneField(Site, primary_key=True, verbose_name='Site Profile', on_delete=models.CASCADE, related_name = "profile")   
    meta_title = models.CharField(max_length=60, null=True, blank=True)
    meta_description = models.TextField(max_length=500, null=True, blank=True)
    
    visitor_addressing_first = models.CharField(max_length=100, null=True, blank=True)
    visitor_addressing_second = models.CharField(max_length=100, null=True, blank=True)
    
    profile_name = models.CharField(max_length=50, null=True, blank=True)
    profile_title = models.CharField(max_length=250, null=True, blank=True)
    
    email = models.EmailField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    location_geo_code = models.TextField(null=True, blank=True)    
    phone = models.CharField(max_length=16, null=True, blank=True)
    
    name_logo = models.ImageField(upload_to='profile_logo/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)
    name_logo_big = models.ImageField(upload_to='profile_logo/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)
    
    favicon = models.ImageField(upload_to='site_image/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)
    home_page_picture = models.ImageField(upload_to='site_image/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)    
    about_picture = models.ImageField(upload_to='site_image/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)
    mask_icon = models.FileField(upload_to='site_image/', validators=[FileExtensionValidator(['svg'])], null=True, blank=True)    
    
    career_summary = models.TextField(null=True, blank=True)
    education_header = models.TextField(null=True, blank=True)
    education_footer = models.TextField(null=True, blank=True)
    
    blog_page_title = models.TextField(null=True, blank=True)
    blog_page_description = models.TextField(null=True, blank=True)
    blog_page_picture = models.FileField(upload_to='site_img_files/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)
    
    project_page_title = models.TextField(null=True, blank=True)
    project_page_description = models.TextField(null=True, blank=True)
    project_page_picture = models.FileField(upload_to='site_img_files/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)
    
    
    service_page_title = models.TextField(null=True, blank=True)
    service_page_description = models.TextField(null=True, blank=True)
    service_page_picture = models.FileField(upload_to='site_img_files/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True)
    
    contact_page_title = models.TextField(null=True, blank=True)
    contact_page_description = models.TextField(null=True, blank=True)
    contact_page_picture = models.FileField(upload_to='site_img_files/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], null=True, blank=True) 
    
    youtube_intro_id =  models.CharField(max_length=250, null=True, blank=True)
    
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)    
    instagram_link = models.URLField(null=True, blank=True)  
    github_link = models.URLField(null=True, blank=True)    
    youtube_link = models.URLField(null=True, blank=True)      
    upwork_link = models.URLField(null=True, blank=True)    
    
    years_of_experience = models.IntegerField(default=0)    
    number_of_industries_works = models.IntegerField(default=0)    
    number_of_clients = models.IntegerField(default=0)    
    
    languages = models.TextField(help_text='Comma Separated', null=True, blank=True) 
    interest = models.TextField(help_text='Comma Separated', null=True, blank=True) 
    
    image_fields_to_optimize = [
            'favicon',           
            'contact_page_picture', 
            'service_page_picture',
            'project_page_picture',
            'blog_page_picture'       
                        
        ]
    
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()    



    
                          
 


class Experience(models.Model):
    """
    Represents an individual's work experience.
    """
    EXPERIENCE_CHOICES = [
        ('freelance', 'Freelance'),
        ('full_time', 'Full time'),
        ('part_time', 'Part time'),
        ('contractual', 'Contractual'),
        ('remote', 'Remote'),
    ]
    
    MARQUEE_DIRECTION = [
        ('left', 'left'),
        ('right', 'right'),

    ]
    
    responsibility_or_designation = models.CharField(max_length=100)
    company_or_workplace = models.CharField(max_length=200)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default="full_time")    
    worked_from = models.DateField(null=True, blank=True)
    worked_to = models.DateField(null=True, blank=True)
    currently_working_or_not = models.BooleanField(default=False)
    text_color_class = models.CharField(max_length=20, null=True, blank=True)    
    background_color_class = models.CharField(max_length=20, null=True, blank=True)
    border_color_class = models.CharField(max_length=20, null=True, blank=True)
    col_width_class = models.CharField(max_length=20, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name = "experiences")
    skills_marquee_direction = models.CharField(max_length=20, choices=MARQUEE_DIRECTION, default="left")    
    objects = models.Manager()
    on_site = CurrentSiteManager('site')

    def __str__(self):
        return f"{self.responsibility_or_designation} at {self.company_or_workplace}"
    
    def save(self, *args, **kwargs):   
        if not self.site: 
            self.site = get_current_site() 
        super().save(*args, **kwargs)
        
        
    def get_skills_name_and_percent(self):
        return {skill.name: skill.skill_percent for skill in self.skills_to_experience.all()}
    
    def get_skills_name_and_image(self):
        return {skill.name: skill.icon_image for skill in self.skills_to_experience.all()}

    def get_skills_name(self):
        return self.skills_to_experience.values_list('name', flat=True)

    def get_skills_image(self):
        return self.skills_to_experience.values_list('icon_image', flat=True)
            
    
class WhatDidThere(models.Model):
    """
    Represents specific items related to an experience.
    """
    item = models.TextField()
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name = "what_did")

    def __str__(self):
        return self.item
    
class SkillsAndTools(models.Model):
    """
    Represents skills and tools associated with a site.
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name = "skills_to_site")
    icon_image = models.FileField(upload_to='skills_icons/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp', 'svg'])], null=True, blank=True)
    name = models.CharField(max_length=100)
    skill_percent = models.PositiveIntegerField()
    working_for_years = models.PositiveIntegerField()
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name = "skills_to_experience")
    on_site = CurrentSiteManager('site')
    objects = models.Manager()
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):   
        if not self.site: 
            self.site = get_current_site()
        super().save(*args, **kwargs)        
        if self.icon_image: 
            icon_image = self.icon_image
            ext = str(icon_image).split('.')[-1]        
            if ext in ['png', 'jpg', 'jpeg']:
                optimized_icon_image = optimize_image_for_web(icon_image.path, delete_original = True, width=80)  
                self.icon_image = optimized_icon_image    
                super().save(*args, **kwargs)  
                

class KeyQualification(  
    models.Model
    ):
    title = models.CharField(max_length=150)   
    body = models.TextField(max_length=400)
    institution = models.CharField(max_length=250, null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    continue_here = models.BooleanField(default=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name = "key_qualiicaions")
    on_site = CurrentSiteManager('site')
    objects = models.Manager()
    
    def __str__(self):
        return self.title
        

