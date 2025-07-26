# auth_app/api/email_backend.py

import ssl
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

class UnverifiedTLSBackend(DjangoEmailBackend):
    """
    SMTP-Backend mit STARTTLS, das keine Zertifikatsprüfung macht.
    Nur für lokale Entwicklung!
    """

    def open(self):
        if self.connection:
            return False
        try:
            # 1) Verbindung öffnen ohne local_hostname-Arg
            self.connection = self.connection_class(
                self.host,
                self.port,
                timeout=self.timeout
            )
            # 2) STARTTLS mit unverified Context
            if self.use_tls:
                context = ssl._create_unverified_context()
                self.connection.starttls(context=context)
            # 3) Login, falls eingestellt
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
            return False
