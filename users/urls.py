"""Defines URL patterns for users"""
from django.urls import path, include

app_name = 'users'
urlpatterns = [
    # Include default auth urls so we can use them under base/users/
    path('', include('django.contrib.auth.urls')),
]
