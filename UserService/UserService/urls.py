from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('auth/', include('userauth.urls')),
]