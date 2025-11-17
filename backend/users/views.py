from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


# ===============================
# Register View
# ===============================
class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Creates a new user account.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT token for the new user
        refresh = RefreshToken.for_user(user)
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "tokens": token_data,
            },
            status=status.HTTP_201_CREATED,
        )


# ===============================
# Login View
# ===============================
class LoginView(APIView):
    """
    POST /api/auth/login/
    Authenticates user and returns JWT tokens.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# ===============================
# Logout View
# ===============================
class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Blacklists a refresh token (optional, if you use JWT token blacklist)
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Only works if JWT blacklist app is enabled
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid or missing token."}, status=status.HTTP_400_BAD_REQUEST)


# ===============================
# User Profile View
# ===============================
class UserProfileView(generics.RetrieveAPIView):
    """
    GET /api/auth/me/
    Returns the authenticated user's profile.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
