# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # -----------------------
    # Authentication
    # -----------------------
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # -----------------------
    # POSTS CRUD
    # -----------------------
    path("posts/", views.PostListView.as_view(), name="posts"),
    path("posts/new/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # -----------------------
    # COMMENTS CRUD
    # -----------------------
    path(
        "posts/<int:pk>/comment/new/",
        views.CommentCreateView.as_view(),
        name="comment-create"
    ),
    path(
        "comment/<int:pk>/edit/",
        views.CommentUpdateView.as_view(),
        name="comment-update"
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment-delete"
    ),
]
# COMMENTS
path("post/<int:post_id>/comment/new/", views.comment_create_view, name="comment-create"),
path("comment/<int:pk>/edit/", views.CommentUpdateView.as_view(), name="comment-update"),
path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
