from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.serializers import UserSerializer, RegisterSerializer
from authentication.utils import get_tokens_for_user, CookieJWTAuthentication
from main import settings


class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                response = Response()
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key="access",
                    value=data.get("access"),
                    max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    httponly=True,
                    samesite="none",
                    secure=True,
                )
                response.set_cookie(
                    key="refresh",
                    value=data.get("refresh"),
                    max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                    httponly=True,
                    samesite="none",
                    secure=True,
                )
                response.data = UserSerializer(user).data
                return response
            else:
                return Response(
                    {"error": "User account is inactive"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {
                    "message": "Пользователь не найден",
                    "detail": "Пользователя с таким именем не существует",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class LogoutView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response = Response()
        response.delete_cookie("access", domain="localhost", path="/")
        response.delete_cookie("refresh", domain="localhost", path="/")
        response.status_code = status.HTTP_205_RESET_CONTENT
        return response
