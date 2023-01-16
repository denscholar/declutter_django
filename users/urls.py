from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path("register/", register, name='register'),
    path("login/", login_request, name='login'),
    path("logout/", logout_request, name='logout'),
    path("request-reset-password-form/", RequestResetPassword, name='request-reset-password-form'),
    path("password_reset_confirm/<uidb64>/<token>", password_reset_confirm, name="password_reset_confirm"),
    path("activate/<uidb64>/<token>",  ActivateAccountView.as_view(), name='activate'),
    path("profile/", profile, name='profile')
]