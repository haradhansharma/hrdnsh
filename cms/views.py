import datetime
from pprint import pprint

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.html import strip_tags
from cms.utils import get_paginated_comments
from common.caching import get_categories, get_popular_tags, get_public_blogs
from common.context_processor import site_profile
from .models import *
from .forms import *
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.clickjacking import xframe_options_exempt  
from django.utils.decorators import method_decorator
from django.core.cache import cache

import logging
log =  logging.getLogger('log')

class BlogListView(ListView):
    model = Blog
    template_name = 'cms/blogs.html'
    paginate_by = 2
    
    
    def get_queryset(self):
       
        # Get the default queryset from the parent class
        queryset = self.model.status_objects.published_on_site(self.request).order_by('-created_at')
        
        # Get the search query from the GET parameters
        search_query = self.request.GET.get('q')
        
        if search_query:
            # Filter the queryset based on title or content containing the search query
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        
        # Check if the 'slug' parameter exists in the URL kwargs
        if 'slug' in self.kwargs:
            # Filter the queryset based on the category slug
            queryset = queryset.filter(category__slug=self.kwargs['slug'])
            
        # Check if the 'tagname' parameter exists in the URL kwargs
        if 'tag_id' in self.kwargs:    
            tag = Tag.on_site.get(id=self.kwargs['tag_id'])            
            # Filter the queryset based on the category slug
            queryset = queryset.filter(tags__name__icontains=tag.name)
            tag.increment_view_count()
        
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        profile = site_profile(self.request)   
        profile['meta_title'] = 'Tagged Sense and Publications' if 'tag_id' in self.kwargs else ('Categoraise Sense and Publication' if 'slug' in self.kwargs else profile['blog_page_title'])
        sumamry = profile['blog_page_description']
        profile['meta_description'] = sumamry[:136] + ' ...' if len(sumamry) > 140 else sumamry
  
        profile['meta_image'] = self.request.build_absolute_uri(profile['blog_page_picture'])        
        context['profile'] = profile                     
        context['indicator'] = 'Tagged' if 'tag_id' in self.kwargs else ('Categoraise' if 'slug' in self.kwargs else 'Blogs')
        
        return context
 
# @method_decorator(xframe_options_exempt, name='dispatch')   
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'cms/blog_details.html'
    context_object_name = 'post'
    
    def get_queryset(self):        
        queryset = self.model.status_objects.published_on_site(self.request)        
        return queryset    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'email' : self.request.user.email if self.request.user.is_authenticated else ''}, user=self.request.user)
        
        obj = self.get_object()
        
        obj_tags = obj.tags.all()        
        for tag in obj_tags:
            tag.increment_view_count()
        

        # Get or create a View object to increment view count
        obj.increment_view_count()
        
        view = obj.view.get()
        
 
        post_comments = get_paginated_comments(self.request, obj)       
        context['post_comments'] = post_comments    
        
        
        context['view_count'] = view.count     
        
        profile = site_profile(self.request)   
        profile['meta_title'] = obj.title
        sumamry = strip_tags(obj.summary)
        profile['meta_description'] = sumamry[:136] + ' ...' if len(sumamry) > 140 else sumamry
        obj_picture = obj.main_image
        profile['meta_image'] = self.request.build_absolute_uri(obj_picture.url)        
        context['profile'] = profile  
        
      
        context['latest_blogs'] = get_public_blogs(self.request)[:5]   
        
             
        context['categories'] = get_categories(self.request)         
        
        
        context['popular_tags'] = get_popular_tags(self.request)  

      
        return context

    def post(self, request, *args, **kwargs):      
        
        
        if 'HTTP_HX_REQUEST' in request.META and request.META['HTTP_HX_REQUEST'] == 'true' and 'comment_form' in request.POST:                            
            return self.handle_comment(request)
        elif 'blog_like_action' in request.POST:
            return self.handle_blog_like(request)
        elif 'comment_like_action' in request.POST:
            return self.handle_comment_like(request)
        # return super().post(request, *args, **kwargs)

    def handle_comment(self, request): 
        blog_post = self.get_object()
        form =   CommentForm(request.POST, user=request.user)   
        if form.is_valid():
            body =  form.cleaned_data['body']   
            email =  request.user.email if request.user.is_authenticated else form.cleaned_data['email']       
            blog_post.add_comment(request.site, email, body)
        else:
            return redirect(reverse('cms:blog_comments_block', kwargs={'post_id':blog_post.id, 'has_error':'yes'}))
        if 'HTTP_HX_REQUEST' in request.META and request.META['HTTP_HX_REQUEST'] == 'true':            
            return redirect(reverse('cms:blog_comments_block', kwargs={'post_id':blog_post.id, 'has_error':'no'}))
        else:
            return redirect(blog_post.get_absolute_url())

    def handle_blog_like(self, request):
        blog_post = self.get_object()
        user = request.user
        like_action = request.POST.get('like_action')
        if like_action == 'like':
            blog_post.add_like(user)
        elif like_action == 'unlike':
            blog_post.remove_like(user)
        return redirect(blog_post.get_absolute_url())
    
    def handle_comment_like(self, request):
        comment = self.get_comment()
        user = request.user
        like_action = request.POST.get('like_action')
        if like_action == 'like':
            comment.add_like(user)
        elif like_action == 'unlike':
            comment.remove_like(user)
        return redirect(self.get_object().get_absolute_url())
  

#htmx respons  
def blog_comments_block(request, *args, **kwargs):
    model = Blog
    post_id = kwargs['post_id']
    has_error = kwargs['has_error']
    
    if has_error == 'yes':
        msg = 'Form has error! not submitted!'
    if has_error == 'no':
        msg = 'Form submitted!'       
    
    obj = model.status_objects.published_on_site(request).prefetch_related('comments').get(id=post_id)
    post_comments = get_paginated_comments(request, obj)
    
    context = {}
    context['post'] = obj    
    context['msg'] = msg              
    context['post_comments'] = post_comments  
    context['comment_form'] = CommentForm(initial={'email' : request.user.email if request.user.is_authenticated else ''}, user=request.user)                 
    return render(request, 'includes/comments_and_form.html', context)

#htmx respons  
def edit_delete_comment(request, id):
    if not request.user.is_staff:
        try:
            comment = Comment.on_site.get(id=id, email=request.user.email)
        except:
            comment = Comment.on_site.get(id=id)
            login_url = reverse('account:login')
            context = {
                'comment' : comment,
                'err' : f'Please <a href={login_url}>LOGIN</a> using {comment.email} to edit/delete the comment!'
            }
            return render(request, 'includes/comment.html', context)
        
    comment = Comment.on_site.get(id=id)
    if request.method == 'GET':
        
        comment_edit_form = CommentEditForm(initial={'body':comment.body})
        context = {
            'comment' : comment,
            'comment_edit_form' : comment_edit_form
        }
        return render(request, 'includes/comment_edit.html', context)
    
    if request.method == 'POST': 
        comment_edit_form = CommentEditForm(request.POST)   
        if comment_edit_form.is_valid():            
            comment.body = comment_edit_form.cleaned_data['body']
            comment.save()
            comment = Comment.on_site.get(id=id)
            context = {
                'comment' : comment
            }
            return render(request, 'includes/comment.html', context)
        
    if request.method == 'DELETE': 
        comment.delete()
        return HttpResponse('<small class="text-danger fs-6">deleted!</small>')
        
    
    
    
