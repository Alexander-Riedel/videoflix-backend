"""
auth_app.api.email_backend
~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom email backend that disables SSL certificate verification for STARTTLS connections.
Intended for local development and testing only. **DO NOT USE IN PRODUCTION!**
"""

import ssl
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend


class UnverifiedTLSBackend(DjangoEmailBackend):
    """
    Custom SMTP email backend with STARTTLS that skips certificate verification.

    WARNING:
        This backend disables SSL certificate verification and is therefore insecure.
        Use only in a local development environment.
    """

    def open(self):
        """
        Opens a connection to the SMTP server using STARTTLS with an unverified SSL context.

        Returns:
            bool: True if connection was successfully established, False otherwise.
        """
        if self.connection:
            return False

        try:
            # Connect to the SMTP server without specifying local_hostname
            self.connection = self.connection_class(
                self.host,
                self.port,
                timeout=self.timeout
            )

            # Use STARTTLS with unverified SSL context
            if self.use_tls:
                context = ssl._create_unverified_context()
                self.connection.starttls(context=context)

            # Authenticate if credentials are set
            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True

        except Exception:
            if not self.fail_silently:
                raise
            return False
