"""Defines URL patterns for users"""
from django.urls import path, include
# from the current app (users), import views.py
from . import views

app_name = 'users'
urlpatterns = [
    # Include default auth urls so we can use them under base/users/
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
]
