from django_filters.rest_framework import FilterSet

from cms.models import Blog


class BlogFilter(FilterSet):
  class Meta:
    model = Blog
    fields = {
      'title': ['iexact'],
      'body': ['iexact'],
      
 
    }