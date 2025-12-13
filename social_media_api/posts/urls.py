from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    LikePostView,
    UnlikePostView,
)

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),

    # Like / Unlike endpoints
    path("posts/<int:pk>/like/", LikePostView.as_view(), name="post-like"),
    path("posts/<int:pk>/unlike/", UnlikePostView.as_view(), name="post-unlike"),
]
