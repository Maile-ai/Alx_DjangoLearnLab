from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    feed,
    like_post,
    unlike_post,
)

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),

    # Feed endpoint
    path("feed/", feed, name="feed"),

    # Like / Unlike endpoints
    path("posts/<int:pk>/like/", like_post, name="post-like"),
    path("posts/<int:pk>/unlike/", unlike_post, name="post-unlike"),
]
