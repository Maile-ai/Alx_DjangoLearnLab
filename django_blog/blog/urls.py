from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # Blog posts
    path("post/", views.PostListView.as_view(), name="posts"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

   # COMMENT ROUTES
path("post/<int:post_id>/comments/new/", views.comment_create, name="comment-create"),
path("comments/<int:pk>/edit/", views.CommentUpdateView.as_view(), name="comment-update"),
path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),

]
