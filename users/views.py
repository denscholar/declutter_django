from django.shortcuts import  render, redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def register(request):
    context = {} 
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful; please, login" )
            return redirect("users:login")
        else:
            CustomUserCreationForm()
    form = CustomUserCreationForm()

    context = {
        'form':form
    }
    
    return render (request, "users/register.html", context)

def login_request(request):
    context = {}
    if request.method == 'POST':
        login_form = CustomUserLoginForm(request.POST)
        if login_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in successfully")
                return redirect("pages:home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    login_form = CustomUserLoginForm()
    context = {
        'login_form': login_form
    }
    return render(request, "users/login.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect("pages:home")