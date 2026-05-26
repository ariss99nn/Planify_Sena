from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(email: str, code: str, expiry_minutes: int = 10) -> None:
    """Envía el código de verificación de correo al registrarse."""
    send_mail(
        subject='Verifica tu correo — Planify',
        message=(
            f'Tu código de verificación es: {code}\n'
            f'Expira en {expiry_minutes} minutos.\n\n'
            f'Si no creaste esta cuenta, ignora este mensaje.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def send_password_reset_email(email: str, token, expiry_minutes: int = None) -> None:
    """Envía el enlace de restablecimiento de contraseña."""
    # ✅ Lee el tiempo real desde settings para no mentirle al usuario
    if expiry_minutes is None:
        expiry_hours = getattr(settings, 'PASSWORD_RESET_EXPIRY_HOURS', 2)
        expiry_minutes = int(expiry_hours) * 60

    reset_url = f"{settings.FRONTEND_URL}/#/reset-password/{token}"

    send_mail(
        subject='Restablecer contraseña — Planify',
        message=(
            f'Usa este enlace para restablecer tu contraseña:\n\n'
            f'{reset_url}\n\n'
            f'Expira en {expiry_minutes // 60} hora(s).\n\n'
            f'Si no solicitaste esto, ignora este mensaje.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def send_email_change_email(email: str, code: str, expiry_minutes: int = 10) -> None:
    """Envía el código de confirmación de cambio de correo."""
    send_mail(
        subject='Confirma tu nuevo correo — Planify',
        message=(
            f'Tu código de confirmación es: {code}\n'
            f'Expira en {expiry_minutes} minutos.\n\n'
            f'Si no solicitaste este cambio, contacta al administrador.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )