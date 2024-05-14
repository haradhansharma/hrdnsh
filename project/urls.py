from django.urls import path
from .views import *
app_name = 'project'

urlpatterns = [
    path('', ProjectHomeView.as_view(), name='home'),
    path('<slug:slug>', ProjectDetailView.as_view(), name='details'),
    path('category/<slug>/', ProjectHomeView.as_view(), name='project_category'),   
]
