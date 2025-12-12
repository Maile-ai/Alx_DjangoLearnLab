from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from notifications.utils import create_notification_for_like


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    # Fetch posts from users the current user follows
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        return Response({"detail": "Already liked"}, status=status.HTTP_200_OK)

    # Create notification for the post author (unless user likes own post)
    create_notification_for_like(actor=user, recipient=post.author, post=post)

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
