from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.models import Site

from common.models import SiteProfile

   
class NonListModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,  
    GenericViewSet
):     
    pass   





    
            
            
    
            
# class CustomModelViewSet(
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.ListModelMixin,
#     GenericViewSet
# ):
#     """
#     A custom viewset that provides default `create()`, `retrieve()`, `update()`,
#     `partial_update()`, `destroy()` and `list()` actions with site validation.
#     """
    
#     queryset = Site.objects.all()
#     serializer_class = SiteSerializer
    
#     def create(self, request, *args, **kwargs):
#         if 'site_id' not in request.data and 'site_domain' not in request.data:
#             return Response({'error': 'site_id or site_domain is required'}, status=status.HTTP_400_BAD_REQUEST)
#         return super().create(request, *args, **kwargs)
    
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.site_id != request.data.get('site_id') and instance.site_domain != request.data.get('site_domain'):
#             return Response({'error': 'Not authorized to access this resource'}, status=status.HTTP_403_FORBIDDEN)
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
    
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.site_id != request.data.get('site_id') and instance.site_domain != request.data.get('site_domain'):
#             return Response({'error': 'Not authorized to update this resource'}, status=status.HTTP_403_FORBIDDEN)
#         return super().update(request, *args, **kwargs)
    
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.site_id != request.data.get('site_id') and instance.site_domain != request.data.get('site_domain'):
#             return Response({'error': 'Not authorized to delete this resource'}, status=status.HTTP_403_FORBIDDEN)
#         return super().destroy(request, *args, **kwargs)