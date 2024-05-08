import random
from django import template
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.utils.text import slugify


register = template.Library()

@register.filter
def json(data):    
    serialized_data = serialize("json", data)
    return serialized_data

@register.filter
def build_commenter(email):
    first_part_of_email = email.split('@')[0]
    
    return slugify(first_part_of_email)
    


@register.simple_tag 
def bg_class(): 
    class_list = [
        {'bgcolor' : 'bg-danger-subtle', 'bordercolor' : 'border-danger', 'textcolor' : 'text-danger', 'linkcolor' : 'link-light', 'linkbgcolor':'bg-danger'},
        {'bgcolor' : 'bg-success-subtle', 'bordercolor' : 'border-success', 'textcolor' : 'text-success', 'linkcolor' : 'link-light', 'linkbgcolor':'bg-success'},
        {'bgcolor' : 'bg-dark-subtle', 'bordercolor' : 'border-dark', 'textcolor' : 'text-dark', 'linkcolor' : 'link-light', 'linkbgcolor':'bg-dark'},
        # {'bgcolor' : 'bg-primary-subtle', 'bordercolor' : 'border-primary', 'textcolor' : 'text-primary', 'linkcolor' : 'link-light', 'linkbgcolor':'bg-primary'},
        {'bgcolor' : 'bg-secondary-subtle', 'bordercolor' : 'border-secondary', 'textcolor' : 'text-secondary', 'linkcolor' : 'link-light', 'linkbgcolor':'bg-secondary'},
        {'bgcolor' : 'bg-warning-subtle', 'bordercolor' : 'border-warning', 'textcolor' : 'text-warning', 'linkcolor' : 'link-primary', 'linkbgcolor':'bg-warning'},        
        
    ]
    return random.choice(class_list)

