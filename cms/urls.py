from django.urls import path
from .views import *
app_name = 'cms'

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/<slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/category/<slug>/', BlogListView.as_view(), name='blog_category'), 
    path('blogs/tag/<int:tag_id>/', BlogListView.as_view(), name='blog_tag'), 
    path('blogs/comments_block/<int:post_id>/<str:has_error>', blog_comments_block, name='blog_comments_block'), 
    path('blogs/comments_edit/<int:id>', edit_delete_comment, name='edit_delete_comment'), 
    
    
    
    
]
