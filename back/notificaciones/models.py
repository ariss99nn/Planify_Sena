# notificaciones/models.py
"""
App de notificaciones: responsable de ENTREGAR alertas al usuario
por canales externos (email, SMS, push).

Arquitectura:
    alertas.Alerta  ->  notificaciones.Notificacion  ->  canal externo
    (fuente de verdad)  (registro de entrega)

Separar ambas permite:
  - Reintentar envios sin duplicar alertas.
  - Soportar multiples canales por alerta.
  - Auditoria de entregas independiente de la logica de negocio.
"""
from django.db import models
from django.conf import settings


class Notificacion(models.Model):
    """
    Registro de un intento de entrega de una Alerta por un canal externo.
    Una misma Alerta puede generar N Notificaciones (una por canal).
    """

    class Canal(models.TextChoices):
        EMAIL = 'EMAIL', 'Email'
        SMS   = 'SMS',   'SMS'
        PUSH  = 'PUSH',  'Push (app)'

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        ENVIADA   = 'ENVIADA',   'Enviada'
        FALLIDA   = 'FALLIDA',   'Fallida'

    alerta = models.ForeignKey(
        'alertas.Alerta',
        on_delete=models.CASCADE,
        related_name='notificaciones',
        help_text='Alerta que origina esta notificacion.',
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones_recibidas',
    )
    canal = models.CharField(
        max_length=10,
        choices=Canal.choices,
        default=Canal.PUSH,
    )
    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        db_index=True,
    )
    intentos = models.PositiveSmallIntegerField(
        default=0,
        help_text='Numero de intentos de entrega realizados.',
    )
    error_detalle = models.TextField(
        blank=True,
        help_text='Detalle del ultimo error si estado=FALLIDA.',
    )
    tarea_id = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='ID de tarea Celery para rastreo/cancelacion.',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio    = models.DateTimeField(
        null=True, blank=True,
        help_text='Momento en que se confirmo el envio exitoso.',
    )

    class Meta:
        verbose_name        = 'Notificacion'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estado', 'canal']),
            models.Index(fields=['destinatario', 'estado']),
        ]
        unique_together = [('alerta', 'destinatario', 'canal')]

    def __str__(self):
        return (
            f"Notif. {self.canal} -> {self.destinatario_id} "
            f"[{self.get_estado_display()}]"
        )