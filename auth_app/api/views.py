"""
auth_app.api.views
~~~~~~~~~~~~~~~~~~

This module contains views for user registration, activation, authentication,
logout, token refresh, and password reset functionality.

All views follow Django REST Framework conventions and return appropriate
HTTP responses. Tokens are handled using SimpleJWT.
"""

from django.contrib.auth.models import User
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    SetNewPasswordSerializer
)
from .utils import send_activation_email, send_password_reset_email


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Sends an activation email after successful registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        self.activation_token = send_activation_email(user, self.request)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'user': {
                'id': response.data['id'],
                'email': response.data['email']
            },
            'token': self.activation_token
        }, status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    """
    API endpoint to activate a user account via email token.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'message': 'Invalid link.'}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account successfully activated.'}, status=200)

        return Response({'message': 'Activation failed.'}, status=400)


class LoginView(APIView):
    """
    API endpoint to authenticate a user and return JWT tokens via cookies.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials.'}, status=400)

        if not user.check_password(password) or not user.is_active:
            return Response({'detail': 'Invalid credentials or inactive account.'}, status=400)

        refresh = RefreshToken.for_user(user)

        response = Response({
            'detail': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username
            }
        }, status=200)
        response.set_cookie('access_token', str(refresh.access_token), httponly=True)
        response.set_cookie('refresh_token', str(refresh), httponly=True)
        return response


class LogoutView(APIView):
    """
    API endpoint to logout a user by blacklisting the refresh token and clearing cookies.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token missing.'}, status=400)

        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response({
            'detail': 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'
        }, status=200)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    API endpoint to refresh the access token using a refresh token stored in cookies.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token missing.'}, status=400)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'detail': str(e)}, status=401)

        access_token = serializer.validated_data.get('access')
        response = Response({
            'detail': 'Token refreshed',
            'access': access_token
        })

        if access_token:
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )

        return response


class PasswordResetView(APIView):
    """
    API endpoint to request a password reset email.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            send_password_reset_email(user, request)
        except User.DoesNotExist:
            pass  # Prevent user enumeration

        return Response({
            'detail': 'An email has been sent to reset your password.'
        }, status=200)


class PasswordConfirmView(APIView):
    """
    API endpoint to reset password using a token from the password reset email.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid link.'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid token.'}, status=400)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Your password has been successfully reset.'}, status=200)
