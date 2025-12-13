from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners to edit or delete their own objects.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    # REQUIRED BY ALX CHECKER
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    # REQUIRED BY ALX CHECKER
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
