from django.conf import settings
from django.db import models
from datetime import date
from django.urls import reverse
from taggit_autosuggest.managers import TaggableManager
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sitemaps import ping_google



class ExtendSite(models.Model):
    site = models.OneToOneField(Site, primary_key=True, related_name='profiles', verbose_name='site', on_delete=models.CASCADE)
    site_meta = models.CharField(max_length=256)
    site_description = models.TextField(max_length=500)
    site_meta_tag =TaggableManager('Meta Tag')
    site_favicon = models.ImageField(upload_to='site_image')
    site_logo = models.ImageField(upload_to='site_image')
    common_slogan = models.CharField(max_length=150, default='Multitasking Living Machine')
    og_image = models.ImageField(upload_to='site_image')
    picture = models.ImageField(upload_to='card_image')
    birth_day = models.DateField(default='1980-07-11')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    last_degree = models.CharField(max_length=256)
    current_location=models.CharField(max_length=120)
    facebook_link = models.URLField()
    twitter_link = models.URLField()
    linkedin_link = models.URLField()
    github_link = models.URLField()
    upwork_link = models.URLField()
    web_address = models.URLField()
    
    # custom email setting under site package
    email_host = models.CharField(max_length=256)
    email_port = models.CharField(max_length=256)
    email_host_user = models.EmailField()
    email_host_pass = models.CharField(max_length=256) 
    
    # It is implemented for future roadmap
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()   
    
# It s standalone, created for future roadmap   
class EmailTemplate(models.Model):
    TYPE_CHOICE = (
        ('contact','Contact'),
        ('signup', 'Signup'),
        ('service_inquery','service_inquery'),
    )
    email_type = models.CharField(max_length=50, choices=TYPE_CHOICE, default='contact', unique=True)
    to_subject=models.CharField(max_length=256)
    to_message=models.TextField(max_length=1000)
    signature = models.TextField(max_length=500)
    
    def __str__(self):
        return self.email_type
    
# contact are associated with site for future roadmap    
class Contacts(models.Model):
    site = models.ForeignKey(Site, related_name='contacts', verbose_name='ContactsTo', on_delete=models.CASCADE, default=settings.SITE_ID)
    name = models.CharField(max_length=100, verbose_name='Enter Name' ) 
    email = models.EmailField(unique=False, verbose_name='Enter Email')
    subject = models.CharField(max_length=256, verbose_name='Subject')
    message = models.TextField(max_length=1000, verbose_name='Messages')
    def __str__(self):
        return self.message
    
    
#  as the app for personal site and site meta held the information of person so it is associated with site   
class Interest(models.Model):
    site = models.ForeignKey(Site, related_name='interest', verbose_name='site interest', on_delete=models.CASCADE)
    name=models.CharField(max_length=120)    
    icon_color=models.CharField(max_length=120, default='#2c2c2c;')
    
    
#  as the app for personal site and site meta held the information of person so it is associated with site       
class Testimonial(models.Model):
    site = models.ForeignKey(Site, related_name='testi', verbose_name='site testimonial', on_delete=models.CASCADE)
    feedback=models.TextField(max_length=500)
    picture=models.ImageField(upload_to='testi_image')
    name=models.CharField(max_length=256)
    job_title=models.CharField(max_length=256)
    def __str__(self) -> str:
        return self.name
    
    
# The features of the site revolve around it
class Card(models.Model):
    MODE_CHOICE = (
        ('professional', 'Professional'),
        ('passionate', 'Passionate'),
    )
    card_type = models.CharField(max_length=20, choices=MODE_CHOICE, default='professional', unique=True)
    full_name = models.CharField(max_length=100, help_text='Write your full name')
    short_title = models.CharField(max_length=150)
    cv_image =   models.ImageField(upload_to='cv_image')
    cv_logo =  models.ImageField(upload_to='cv_image')  
    objective = models.TextField()
    card_front = models.ImageField(upload_to='card_image')
    card_back = models.ImageField(upload_to='card_image')      
    aviable_for = TaggableManager('Avialable For',help_text='Write Comma separated Contract Type eg: remote etc')    
    slug = models.SlugField(unique=True, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.card_type    
    
    # due to front end design it is necessary. as a first project worked and thinked simply.
    def get_skills_area(self):
        area1 = Skills.objects.filter(card__exact=self.id, area__exact = 'area1').order_by('title')
        area2 = Skills.objects.filter(card__exact=self.id, area__exact = 'area2').order_by('title')
        areas = {
            'area1':area1,
            'area2':area2,
        }        
        return areas
    
    # due to front end design it is necessary. as a first project worked and thinked simply.  
    def get_service_title(self):
        services = Service.objects.filter(card__exact=self.id)       
        block1 = services[:(services.count())/2]#1/2 of total
        block2 = services[(services.count())/2:]#It is still to check, here should 2+1
        context ={
            'block1':block1,
            'block2':block2
            }
        return context
    
    #I need to group experience based on jop type in pdf cv
    def get_experiences(self):   
        experiences = Experience.objects.values('job_type', 'title','start_from','responsibilities').order_by('job_type', 'start_from').filter(card__exact=self.id)
        context ={
            'experiences':experiences,                             
        }
        return context    
    
    def get_absolute_url(self):
        return reverse("card:card-detail", args=[str(self.slug)])
    
    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
    
#Extendable hiring facility  
class HireMe(models.Model):
    site = models.CharField(max_length=256)
    site_link = models.URLField()
    card=models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, help_text='Select Card')
    
    
#Although it should not the name I decide but I want to keep it as it is   
class PrCategory(models.Model):
    name=models.CharField(max_length=200, help_text='Enter Profile Category')
    card=models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, help_text='Select Card')
    handy_tools = TaggableManager('Handy Tools',help_text='Write Comma separated Contract Type eg: remote etc')  

    def __str__(self):
        return self.name
    
class Skills(models.Model):
    AREA_CHOICE = (#It is just for frontend design so hard coded
        ('area1', 'Area1'),
        ('area2', 'Area2'),
    )
    title = models.CharField(max_length=200, help_text='Enter Skills Name')
    card=models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, help_text='Select Card')
    proficiency = models.IntegerField(help_text='Enter digit only!')
    practicing_from = models.DateField(null=True, blank=True)
    area = models.CharField(max_length=20, choices=AREA_CHOICE,  unique=False)
    show_in_card = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('practicing_from',) 
        
class Experience(models.Model):
    JOB_TYPE = (# Roadmap to refine
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('freelancing', 'Freelancing'),
        ('self_business', 'Self Business'),
    )
    title = models.CharField(max_length=200, help_text='Enter Experience title')
    slug = models.SlugField(unique=True, null=False, blank=False)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE, default='full-time')
    card=models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, help_text='Select Card')
    responsibilities = models.TextField()
    start_from = models.DateField(null=True, blank=True)
    color_code = models.CharField(max_length=20, help_text="Write like '#2c2c2c;' with hash and semicolon ", default='#2c2c2c')#to control the design
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('start_from',)  
        
    def get_absolute_url(self):
        return reverse("card:experience-detail", args=[str(self.slug)])
    
    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
        
class Works(models.Model):
    STATUS_CHOICE = (#roadmap to refine
        ('complete', 'Complete'),
        ('under_development', 'Under Development'),
    )
    title = models.CharField(max_length=200, help_text='Enter Works title')
    card=models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, help_text='Select Card')
    slug = models.SlugField(unique=True, null=False, blank=False)
    picture=models.ImageField(upload_to='works')
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='under_development')
    description=models.TextField(max_length=1000)
    Tag = TaggableManager('Tag',help_text='Write Comma separated work Type eg: eCommerce, Knitwears etc')
    completed=models.DateField(null=True, blank=True)
    work_url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    class Meta:
        ordering = ('-status',)   
             
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("card:works-detail", args=[str(self.slug)])
    
    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
    
# This dynamic feature currently use as manual service type have future roadmap    
class Service(models.Model):
    card=models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, help_text='Select Card')
    incon_class = models.CharField(max_length=256)#to control the design
    title = models.CharField(max_length=256)
    description=models.TextField(max_length=1000)
    slug = models.SlugField(unique=True, null=False, blank=False, default='s1')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("card:service-request", args=[str(self.slug)])
    
    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()#update to google when new data add
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
    
    
#Additional to the Service to get query to recover current necessity. have future roadmap    
class ServiceInquery(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, help_text='Select Service name')
    name = models.CharField(max_length=256)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    message = models.TextField()
    
    def __str__(self) -> str:
        return self.name
    
    
       

    
    
    
    