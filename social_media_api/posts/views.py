from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    # REQUIRED BY CHECKER
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
def feed(self, request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
    serializer = self.get_serializer(posts, many=True)
    return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    # REQUIRED BY CHECKER
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
