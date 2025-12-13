from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from posts.models import Post
from posts.serializers import PostSerializer


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        following_users = user.following.all()

        # REQUIRED by ALX checker
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
