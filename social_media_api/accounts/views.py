from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()


# -------------------------------
# Registration (public)
# -------------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # <-- allow public access

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token = Token.objects.get(user=user)
        return Response({
            "message": "Registration successful",
            "token": token.key,
            "user": response.data
        })


# -------------------------------
# Login (public)
# -------------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []  # <-- allow public access

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


# -------------------------------
# User Profile (requires login)
# -------------------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# -------------------------------
# Follow
# -------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target_user = User.objects.filter(id=user_id).first()
    if not target_user:
        return Response({"detail": "User not found."}, status=404)

    if target_user == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=400)

    request.user.following.add(target_user)
    return Response({"detail": f"You are now following {target_user.username}."})


# -------------------------------
# Unfollow
# -------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target_user = User.objects.filter(id=user_id).first()
    if not target_user:
        return Response({"detail": "User not found."}, status=404)

    if target_user == request.user:
        return Response({"detail": "You cannot unfollow yourself."}, status=400)

    request.user.following.remove(target_user)
    return Response({"detail": f"You have unfollowed {target_user.username}."})
