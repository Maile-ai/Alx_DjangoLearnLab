from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

CustomUser = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(username=response.data["username"])
        token = Token.objects.get(user=user)
        return Response({
            "message": "Registration successful",
            "token": token.key,
            "user": response.data
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "token": token.key,
            "username": user.username
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ------------------------------
# Follow / Unfollow (Class-Based)
# ------------------------------

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        queryset = CustomUser.objects.all()

        try:
            target_user = queryset.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        request.user.following.add(target_user)
        return Response({"detail": f"You are now following {target_user.username}."})


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        queryset = CustomUser.objects.all()

        try:
            target_user = queryset.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        request.user.following.remove(target_user)
        return Response({"detail": f"You have unfollowed {target_user.username}."})


# ------------------------------
# Follow / Unfollow (Function Wrappers)
# REQUIRED for urls.py imports
# ------------------------------

def follow_user(request, user_id):
    view = FollowUserView.as_view()
    return view(request, user_id=user_id)


def unfollow_user(request, user_id):
    view = UnfollowUserView.as_view()
    return view(request, user_id=user_id)
