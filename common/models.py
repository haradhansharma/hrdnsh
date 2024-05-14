import os
from PIL import Image
from io import BytesIO
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import FileExtensionValidator, ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.text import slugify
from account.models import User
from cms.managers import PublishManager
from cms.mixins import CategoryMixin, DateTimeMixin, ImageMixin, SaveAndImageOptimizationMixin, SiteAutorMixin, SlugMixin, StatusMixin, TitleBodyMixin
from common.utils import optimize_image_for_web
import zipfile
from django.core.cache import cache
from django.core.mail import get_connection
from django.contrib import messages
from django.core.files.storage import default_storage
import smtplib

from django.core.exceptions import ValidationError
from django.core.mail.backends.smtp import EmailBackend
from guardian.shortcuts import assign_perm, get_users_with_perms


class SiteProfile(SaveAndImageOptimizationMixin, models.Model):    
    site = models.OneToOneField(Site, primary_key=True, verbose_name='PK', on_delete=models.CASCADE, related_name = "profile", help_text='Primary Key of the Profile')   
    associate_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='associated_profile' )
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
    
    favicon = models.ImageField(upload_to='site_image/', validators=[FileExtensionValidator(['ico'])], null=True, blank=True)
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
            'contact_page_picture', 
            'service_page_picture',
            'project_page_picture',
            'blog_page_picture'       
                        
        ]
    
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()    
    
    class Meta:
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]


class SelectedTemplate(models.Model):
    profile =  models.OneToOneField(SiteProfile, primary_key=True, on_delete=models.CASCADE, related_name='selected_template', verbose_name='PK', help_text="Primary Key of the Selected Template")
    template = models.ForeignKey(
        'common.Template', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='profile_template',
        limit_choices_to={'status': 'public'}
        )
        
    def save(self, *args, **kwargs):           
        super().save(*args, **kwargs)   
        from hrdnsh.middleware import modify_site_cache_global
        modify_site_cache_global()     
        
    class Meta:
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
     
 


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
    
    
    class Meta:
        ordering = ['responsibility_or_designation', 'company_or_workplace']
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]

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
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name = "what_did")
    item = models.TextField()
    

    def __str__(self):
        return self.item
    
    class Meta:
        ordering = ['item']
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]

    
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
        """
        Overrides the default save method to delete the old image file when updating an instance.
        """
        # Get the old image path (if it exists) before saving the new one
        old_image_path = self.icon_image.path if self.pk and self.icon_image else None

        super().save(*args, **kwargs)  # Save the model instance first

        # Check if the image field has changed (new image uploaded)
        if self.icon_image and old_image_path and old_image_path != self.icon_image.path:
            # Delete the old image file using the default storage
            if default_storage.exists(old_image_path):
                default_storage.delete(old_image_path)
                
    class Meta:
        ordering = ['name', 'skill_percent']
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]

    
   
                

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
    
    
    class Meta:
        ordering = ['-from_date','title']
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]
    


class Template(
    TitleBodyMixin,
    SlugMixin,   
    ImageMixin, 
    DateTimeMixin,  
    StatusMixin,
    SaveAndImageOptimizationMixin, #if need to edit save method look here
    models.Model
    ):        
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='uploaded_templates')
    template_zip = models.FileField(upload_to=settings.TEMP_DIR, blank=True) 
    template_dir = models.TextField(null=True, blank=True)
    premium = models.BooleanField(default=False)    
    
    
    
    image_fields_to_optimize = ['main_image']
    
    objects = models.Manager()  
  
    status_objects = PublishManager()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)         
        if self.template_zip:
            with zipfile.ZipFile(self.template_zip.path, 'r') as zip_ref:
                # extracted_path = os.path.join(settings.TEMP_UPLOAD_DIR, os.path.splitext(os.path.basename(self.template_zip.name))[0])
                extracting_path = settings.TEMP_UPLOAD_DIR                
                zip_ref.extractall(extracting_path)
                zip_ref.close() 
                
                template_name = os.path.split(os.path.splitext(self.template_zip.name)[0])[-1]
                
                parent_folder = os.path.commonprefix(zip_ref.namelist()).split('/')[0]                
                extracted_path = os.path.join(settings.TEMP_UPLOAD_DIR, parent_folder)
                new_extracted_path = os.path.join(settings.TEMP_UPLOAD_DIR, template_name)
                os.rename(extracted_path, new_extracted_path)
                
                self.template_dir = template_name
                self.template_zip.delete(save=False)                             
        super().save(*args, **kwargs)
        
        
    class Meta:
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]

        
    
  
        

    def __str__(self):
        return f"Template: {self.title}"
    

def validate_file_size(file):
    # 5MB file size limit
    max_size = 500 * 1024
    if file.size > max_size:
        raise ValidationError("The maximum file size that can be uploaded is %s. Your file size is %s." %(filesizeformat(max_size), filesizeformat(file.size)))

    
    
    
class ExtraProfileImages(models.Model):
    profile =  models.ForeignKey(SiteProfile, on_delete=models.CASCADE, related_name='extra_images')
    key_name = models.CharField(max_length=150)
    image = models.FileField(
        upload_to='profile_template_images/', 
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp', 'svg']),
            validate_file_size
            ], 
        null=True,
        blank = True
      
        )
    
    def __str__(self):
        return f"File Key: {self.key_name}"
    
    class Meta:
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]

    


class PersonalizedEmailSetting(models.Model):
    site = models.OneToOneField(Site, primary_key=True, on_delete=models.CASCADE, related_name='personalized_setting')
    email = models.EmailField('Sender Email', null=True, blank=True, help_text="If provided Acknowledgement of contact form will be sent from this email and Contact Notification will receive here.")
    host = models.CharField(max_length=250, null=True, blank=True, help_text='Email will sent using this host')
    port = models.IntegerField('SMTP port', null=True, blank=True, help_text="SMTP port from your email configuration settings to sent email")
    host_user = models.CharField(help_text="Email user", null=True, blank=True, max_length=150)
    host_password = models.CharField(max_length=250, null=True, blank=True, help_text="Email Password")
    acknowledge_message = models.TextField(max_length=500, null=True, blank=True, help_text="Do not include Addrssing Or Email Signature. Just Write After Dear Client and before Best Regards")
    
    def __str__(self):
        return f"Email Settings For: {self.site.domain}"
    
    class Meta:
        permissions = [
            ("can_access_all", "Can Access all objects"),
        ]

    

    def clean(self):
        """
        Checks the validity of email credentials during saving.
        Raises ValidationError if connection or authentication fails.
        """

        try:
            # Create a temporary EmailBackend instance for testing
            backend = EmailBackend(
                host=self.host,
                port=self.port,
                username=self.host_user,
                password=self.host_password,
                use_ssl=True,
                use_tls=False  
                
            )
            connection = backend.open()   
            if connection:
                backend.close() 

        except (smtplib.SMTPException, smtplib.SMTPAuthenticationError) as e:
            message = f"Email connection failed: {str(e)}"
            raise ValidationError(message)

        return super().clean()


