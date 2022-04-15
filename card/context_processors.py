from .models import *
from haradhan import settings  
      

def add_variable_to_context(request):
    try:
        obj = ExtendSite.on_site.all()[0] 
        interest = Interest.objects.all()
        testi = Testimonial.objects.all()
    except:
        obj = None
        interest = None
        testi = None
    return {
        'site': obj,
        'meta_title': obj.site_meta,
        'meta_slogan': obj.common_slogan,
        'meta_description': obj.site_description,
        'meta_tags' : [t.name for t in obj.site_meta_tag.all()], 
        'meta_image': obj.og_image,
        'favicon': obj.site_favicon,
        'interest':interest,
        'testi':testi
    }
    
