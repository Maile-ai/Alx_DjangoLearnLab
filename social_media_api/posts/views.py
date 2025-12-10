from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    # Fetch posts from users the current user follows
    following_users = request.user.following.all()
    
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
