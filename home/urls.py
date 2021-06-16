from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('create_title/', views.create_title, name='create_title'),
    path('', views.home, name='home'),
]
