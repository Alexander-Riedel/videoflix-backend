"""
auth_app.api.utils
~~~~~~~~~~~~~~~~~~

This module provides utility functions for email-based activation and password reset,
as well as helper functions for JWT token generation using SimpleJWT.
"""

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken


def send_activation_email(user, request):
    """
    Sends an account activation email to the user.

    Args:
        user (User): The user instance to activate.
        request (HttpRequest): The request context.

    Returns:
        str: The generated activation token.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    base_url = settings.FRONTEND_URL.rstrip('/')
    activation_url = (
        f"{base_url}/pages/auth/activate.html"
        f"?uid={uidb64}&token={token}"
    )

    subject = 'Activate Your Account'
    message = (
        f"Hello {user.username},\n\n"
        f"Please click the link below to activate your account:\n\n"
        f"{activation_url}\n\n"
        f"If you did not register, you can ignore this email."
    )

    send_mail(
        subject,
        message,
        None,  # uses DEFAULT_FROM_EMAIL
        [user.email],
        fail_silently=False,
    )
    return token


def send_password_reset_email(user, request):
    """
    Sends a password reset email to the user.

    Args:
        user (User): The user requesting a password reset.
        request (HttpRequest): The request context.

    Returns:
        str: The generated password reset token.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    base_url = settings.FRONTEND_URL.rstrip('/')
    reset_url = (
        f"{base_url}/pages/auth/confirm_password.html"
        f"?uid={uidb64}&token={token}"
    )

    subject = 'Reset Your Password'
    message = (
        f"Hello {user.username},\n\n"
        f"To reset your password, please click the link below:\n\n"
        f"{reset_url}\n\n"
        f"If you did not request this, you can ignore this email."
    )

    send_mail(
        subject,
        message,
        None,  # uses DEFAULT_FROM_EMAIL
        [user.email],
        fail_silently=False,
    )
    return token


def get_tokens_for_user(user):
    """
    Generates refresh and access tokens for the authenticated user.

    Args:
        user (User): The user instance.

    Returns:
        dict: A dictionary with 'refresh' and 'access' token strings.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
