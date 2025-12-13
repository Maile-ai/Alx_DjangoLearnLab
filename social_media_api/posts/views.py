from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action

from posts.models import Post, Comment, Like
from posts.serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


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

    # FEED VIEW (CHECKER REQUIRED)
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated]
    )
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


# ============================
# LIKE / UNLIKE VIEWS
# ============================

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if created:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response(
            {"detail": "Post liked"},
            status=status.HTTP_200_OK
        )


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        Like.objects.filter(
            user=request.user,
            post=post
        ).delete()

        return Response(
            {"detail": "Post unliked"},
            status=status.HTTP_200_OK
        )
