from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path("register/", register, name='register'),
    path("login/", login_request, name='login'),
    path("logout/", logout_request, name='logout'),
    path("profile/", profile, name='profile')
]