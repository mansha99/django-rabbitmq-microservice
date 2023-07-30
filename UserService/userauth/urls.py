from django.urls import path
from userauth.views import  RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
]