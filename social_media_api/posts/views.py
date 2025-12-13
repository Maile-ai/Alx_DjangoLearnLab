from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
)
from notifications.utils import create_notification_for_like


# ------------------------------
# ViewSets (required by router)
# ------------------------------

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ------------------------------
# Feed View
# ------------------------------

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


# ------------------------------
# Like / Unlike Views
# ------------------------------

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        return Response({"detail": "Already liked"}, status=status.HTTP_200_OK)

    create_notification_for_like(
        actor=user,
        recipient=post.author,
        post=post,
    )

    return Response({"detail": "Post liked"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    deleted, _ = Like.objects.filter(user=user, post=post).delete()

    if deleted:
        return Response({"detail": "Like removed"}, status=status.HTTP_200_OK)

    return Response({"detail": "No like to remove"}, status=status.HTTP_400_BAD_REQUEST)
