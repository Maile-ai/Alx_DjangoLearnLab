from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm, UserUpdateForm
from .models import Profile

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("blog:profile")
        else:
            messages.error(request, "Fix the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("blog:profile")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "blog/logout.html")


@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
        else:
            messages.error(request, "Please fix the errors.")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "blog/profile.html", {"form": form})
