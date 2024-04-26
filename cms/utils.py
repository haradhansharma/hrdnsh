from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# helper  
def get_paginated_comments(request, obj):        
        post_comments = obj.comments.all()
        paginator = Paginator(post_comments, 5)
        page_number = request.GET.get('page')        
        try:
            post_comments = paginator.page(page_number)
        except PageNotAnInteger:          
            post_comments = paginator.page(1)
        except EmptyPage:        
            post_comments = paginator.page(paginator.num_pages)
            
        return post_comments