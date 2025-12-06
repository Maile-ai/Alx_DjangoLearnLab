# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Profile
    path("profile/", views.profile_view, name="profile"),

    # Posts CRUD
    path("", views.PostListView.as_view(), name="posts"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # Comments CRUD
    path("post/<int:pk>/comments/new/", views.comment_create, name="comment-create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),

    # Tag filtering
    path("tags/<slug:tag_slug>/", views.PostByTagListView.as_view(), name="posts-by-tag"),

    # Search
    path("search/", views.post_search, name="post-search"),
]
