from django.urls import path
from .views import *
app_name = 'contact'

urlpatterns = [
   path('', HomeView.as_view(), name='home'),
   path('success/', success_view, name='success'),
   
]
