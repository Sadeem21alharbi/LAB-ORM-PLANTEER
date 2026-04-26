from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# دالة التسجيل (مستخدم جديد)
def register_view(request):
    if request.method == "POST":
        reg_form = UserCreationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            return redirect("accounts:login_view")
    
    return render(request, "accounts/register.html", {"register_form": UserCreationForm()})

# دالة تسجيل الدخول
def login_view(request):
    if request.method == "POST":
        log_form = AuthenticationForm(data=request.POST)
        if log_form.is_valid():
            user = log_form.get_user()
            login(request, user)
            return redirect("main:home_view")
    
    return render(request, "accounts/register.html", {"register_form": UserCreationForm()})

# دالة تسجيل الخروج
def logout_view(request):
    logout(request)
    return redirect("main:home_view")