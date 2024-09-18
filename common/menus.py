

from django.urls import reverse
from django.core.cache import cache

def mega_menu_items(request): 
    
    menus = cache.get(f"menu_items")
    if menus is not None:
        return menus
    
       
    menu_items = []    
    home = {
        'title' : 'Home',
        'url' : reverse('common:home'),
        'sub_set' : False,
        'icon' : '<i class="icon-home me-2"></i>'
    }
    menu_items.append(home)    
    
    blog = {
        'title' : 'Blogs',
        'url' : reverse('cms:blog_list'),
        'sub_set' : False,
        'icon' : '<i class="icon-book-open me-2"></i>'
    }
    menu_items.append(blog)
    
    project = {
        'title' : 'Projects',
        'url' : reverse('project:home'),
        'sub_set' : False,
        'icon' : '<i class="icon-film me-2"></i>'
    }
    menu_items.append(project)
    
    service = {
        'title' : 'Services',
        'url' : reverse('service:home'),
        'sub_set' : False,
        'icon' : '<i class="icon-bag me-2"></i>'
    }
    menu_items.append(service)
    
    about = {
        'title' : 'About Me',
        'url' : reverse('common:about'),
        'sub_set' : False,
        'icon' : '<i class="icon-present me-2"></i>'
    }
    menu_items.append(about)
    
    contact = {
        'title' : 'Contact',
        'url' : reverse('contact:home'),
        'sub_set' : False,
        'icon' : '<i class="icon-bubbles me-2"></i>'
    }
    menu_items.append(contact)
    
    cache.set(f"menu_items", menu_items)
    
    return menu_items