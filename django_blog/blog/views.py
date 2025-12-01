from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'blog/base.html')
def posts(request):
    return render(request, 'blog/base.html', {"placeholder": "Posts page"})
def login_view(request):
    return render(request, 'blog/base.html', {"placeholder": "Login page works"})

def register_view(request):
    return render(request, 'blog/base.html', {"placeholder": "Register page works"})