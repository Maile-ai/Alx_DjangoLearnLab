# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),


    path("post/", views.PostListView.as_view(), name="posts"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"), 
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"), 
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),  
]
