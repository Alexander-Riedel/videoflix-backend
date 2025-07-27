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
    RegisterSerializer, LoginSerializer,
    PasswordResetSerializer, SetNewPasswordSerializer
)
from .utils import send_activation_email
from .utils import send_password_reset_email

# 1. Registrierung
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # E-Mail versenden und Token merken
        self.activation_token = send_activation_email(user, self.request)

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        return Response({
            'user': {
                'id': resp.data['id'],
                'email': resp.data['email']
            },
            'token': self.activation_token
        }, status=status.HTTP_201_CREATED)


# 2. Aktivierung
class ActivateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'message': 'Ungültiger Link.'}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account successfully activated.'}, status=200)
        return Response({'message': 'Aktivierung fehlgeschlagen.'}, status=400)


# 3. Login
class LoginView(APIView):
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

        if not user.check_password(password):
            return Response({'detail': 'Invalid credentials.'}, status=400)
        if not user.is_active:
            return Response({'detail': 'Account not activated.'}, status=400)

        # JWT-Tokens erstellen
        refresh = RefreshToken.for_user(user)
        response = Response({
            'detail': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username
            }
        }, status=200)
        # HttpOnly-Cookies setzen
        response.set_cookie('access_token', str(refresh.access_token), httponly=True)
        response.set_cookie('refresh_token', str(refresh), httponly=True)
        return response


# 4. Logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh-Token fehlt.'}, status=400)

        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist aktivieren

        response = Response({
            'detail': 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'
        }, status=200)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


# 5. Token Refresh
class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]  # Cookie-Check intern

    def post(self, request, *args, **kwargs):
        # SimpleJWT erwartet das Refresh-Token im Body; wir lesen es aus dem Cookie und packen es um
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh-Token fehlt.'}, status=400)
        request.data._mutable = True
        request.data['refresh'] = refresh_token
        request.data._mutable = False

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200 and 'access' in response.data:
            # Neues Access-Token als Cookie setzen
            response.set_cookie('access_token', response.data['access'], httponly=True)
            response.data = {
                'detail': 'Token refreshed',
                'access': response.data['access']
            }
        return response


# 6. Passwort zurücksetzen (E-Mail versenden)
class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            # Wir versenden jetzt einen expliziten Password-Reset-Link
            send_password_reset_email(user, request)
        except User.DoesNotExist:
            pass  # Sicherheitsmaßnahme: keine Information darüber, ob die E-Mail existiert

        return Response({
            'detail': 'An email has been sent to reset your password.'
        }, status=200)


# 7. Passwort ändern per Token
class PasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Ungültiger Link.'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Ungültiges Token.'}, status=400)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Your Password has been successfully reset.'}, status=200)
