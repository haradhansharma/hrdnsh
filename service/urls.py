from django.urls import path
from .views import *
app_name = 'service'

urlpatterns = [
   path('', ServiceHomeView.as_view(), name='home'),
   path('<slug:slug>/', ServiceDetailView.as_view(), name='details'),
    path('category/<slug>/', ServiceHomeView.as_view(), name='service_category'),   
   
   
]
