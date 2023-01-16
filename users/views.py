from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.models import User
from .models import Profile
from django.views.generic import View

# To activate user account
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError

# For signing email
from django.core.mail import (
    send_mail,
    EmailMultiAlternatives,
    BadHeaderError,
    EmailMessage,
)
from django.conf import settings

import threading
from threading import Thread

# import password generators
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# to generate token
from .utils import TokenGenerator, generate_token

# threading
import threading

# this makes the email delivery veery fast
class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


# threading function


def register(request):
    context = {}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        email = request.POST["email"]
        if form.is_valid():
            # make the user inactive
            user = form.save(commit=False)
            user.is_active = False
            # save the user instance in the database
            user.save()
            # get the current site the user is on
            current_site = get_current_site(request)
            email_subject = "Activate your account"
            message = render_to_string(
                "users/activate.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": generate_token.make_token(user),
                },
            )
            email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, [email]
            )
            EmailThread(email_message).start()
            messages.success(
                request,
                "Registration successful; pleass login with the link sent to your email",
            )
            # return redirect("users:login")
            return render(request, "users/register.html", context)
        else:
            messages.error(request, "Please check credentials")
            CustomUserCreationForm()
    form = CustomUserCreationForm()

    context = {"form": form}

    return render(request, "users/register.html", context)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            return render(request, "users/activatefail.html")

        if generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account activated successfully")
            return redirect("users:login")
        return render(request, "users/activatefail.html")


def login_request(request):
    context = {}
    if request.method == "POST":
        login_form = CustomUserLoginForm(request.POST)
        if login_form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in successfully")
                return redirect("pages:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    login_form = CustomUserLoginForm()
    context = {"login_form": login_form}
    return render(request, "users/login.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect("pages:home")


@login_required
def profile(request):
    context = {}
    return render(request, "users/profile.html", context)


def RequestResetPassword(request):
    context = {}
    if request.method == "POST":
        reset_form = CustomPasswordResetForm(request.POST)
        if reset_form.is_valid():
            email = reset_form.cleaned_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
                current_site = get_current_site(request)
                email_subject = "Reset your password"
                message = render_to_string(
                    "users/reset-user-password.html",
                    {
                        "user": user,
                        "domain": current_site,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": generate_token.make_token(user),
                    },
                )
                email_message = EmailMessage(
                    email_subject, message, settings.EMAIL_HOST_USER, [email]
                )
                EmailThread(email_message).start()
                messages.info(request, "An link has been sent to " + email + ". use it to reset your password.")
                return redirect(reverse("users:request-reset-password-form"))
            except CustomUser.DoesNotExist:
                messages.error(
                    request, "The email address is not associated with any account."
                )
                return redirect(reverse("users:request-reset-password-form"))
    else:
        reset_form = CustomPasswordResetForm()
        context = {"reset_form": reset_form}
    return render(request, "users/request-reset-password-form.html", context)


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        if request.method == "POST":
            confirm_form = CustomPasswordResetConfirmForm(request.POST)
            if confirm_form.is_valid():
                new_password = confirm_form.cleaned_data["new_password"]
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been reset.")
                return redirect("users:login")
        else:
            confirm_form = CustomPasswordResetConfirmForm()
        
        context = {"confirm_form": confirm_form}
        return render(request, "users/password_reset_confirm.html", context)
    else:
        messages.error(request, "The reset password link is invalid or has expired.")
        return redirect("users:password_reset")