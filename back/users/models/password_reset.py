import uuid
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone


class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_resets',
    )

    token = models.UUIDField(default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Restablecimiento de contraseña'
        verbose_name_plural = 'Restablecimientos de contraseña'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'is_used']),
        ]

    def __str__(self):
        return f"Reset de contraseña para {self.user.email} — {'usado' if self.is_used else 'pendiente'}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self):
        """Un token es válido si no fue usado ni expiró."""
        return not self.is_used and not self.is_expired()

    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])

    @staticmethod
    def get_expiration_time():
        # Lee PASSWORD_RESET_EXPIRY_HOURS del .env (default: 2 horas)
        hours = getattr(settings, 'PASSWORD_RESET_EXPIRY_HOURS', 2)
        return timezone.now() + timedelta(hours=int(hours))

    @classmethod
    def invalidate_previous_tokens(cls, user):
        """Invalida todos los tokens pendientes del usuario."""
        cls.objects.filter(user=user, is_used=False).update(is_used=True)