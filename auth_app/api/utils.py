# auth_app/api/utils.py

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken


def send_activation_email(user, request):
    """
    Erzeugt einen Aktivierungs-Token und baut den Frontend-Link:
    FRONTEND_URL/pages/auth/activate.html?uid={uid}&token={token}
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    base = settings.FRONTEND_URL.rstrip('/')
    activate_url = (
        f"{base}/pages/auth/activate.html"
        f"?uid={uidb64}&token={token}"
    )

    subject = 'Aktiviere dein Konto'
    message = (
        f"Hallo {user.username},\n\n"
        f"bitte klicke auf den folgenden Link, um dein Konto zu aktivieren:\n\n"
        f"{activate_url}\n\n"
        "Falls du dich nicht registriert hast, ignoriere diese E-Mail."
    )
    send_mail(
        subject,
        message,
        None,               # DEFAULT_FROM_EMAIL
        [user.email],
        fail_silently=False,
    )
    return token

def send_password_reset_email(user, request):
    """
    Erzeugt einen Reset-Token und baut den Frontend-Link:
    FRONTEND_URL/pages/auth/confirm_password.html?uid={uid}&token={token}
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    base = settings.FRONTEND_URL.rstrip('/')
    reset_url = (
        f"{base}/pages/auth/confirm_password.html"
        f"?uid={uidb64}&token={token}"
    )

    subject = 'Passwort zurücksetzen'
    message = (
        f"Hallo {user.username},\n\n"
        f"um dein Passwort zurückzusetzen, klicke bitte auf den folgenden Link:\n\n"
        f"{reset_url}\n\n"
        "Falls du diese Anfrage nicht gestellt hast, ignoriere diese E-Mail."
    )
    send_mail(
        subject,
        message,
        None,               # DEFAULT_FROM_EMAIL
        [user.email],
        fail_silently=False,
    )
    return token

def get_tokens_for_user(user):
    """
    Erstellt ein Refresh- und ein Access-Token für den übergebenen User.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
