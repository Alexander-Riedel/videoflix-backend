from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken

def send_activation_email(user, request):
    """
    Erzeugt einen Aktivierungs-Token, baut die URL und verschickt eine E-Mail.
    Gibt den Token zurück, damit wir ihn im Response mitgeben können.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activate_path = reverse('auth_app:activate', args=[uidb64, token])
    activate_url = request.build_absolute_uri(activate_path)

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
        None,                 # Absende-Adresse (DEFAULT_FROM_EMAIL aus settings)
        [user.email],         # Empfänger
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
