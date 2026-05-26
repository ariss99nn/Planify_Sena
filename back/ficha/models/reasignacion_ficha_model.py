from django.db import models
from django.conf import settings
from django.db import transaction
from ficha.models.ficha_model import Ficha


class ReasignacionFicha(models.Model):
    
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reasignaciones',
        limit_choices_to={'rol': 'ESTUDIANTE'},
    )
    ficha_origen = models.ForeignKey(
        Ficha,
        on_delete=models.PROTECT,
        related_name='reasignaciones_salida',
    )
    ficha_destino = models.ForeignKey(
        Ficha,
        on_delete=models.PROTECT,
        related_name='reasignaciones_entrada',
    )
    motivo = models.TextField(
        help_text='Motivo de la reasignación (cambio de jornada, cupo, etc.).',
    )
    realizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reasignaciones_realizadas',
        null=True,
        blank=True,
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reasignación de ficha'
        verbose_name_plural = 'Reasignaciones de ficha'
        ordering = ['-fecha']

    def __str__(self):
        return (
            f"{self.estudiante.nombre}: "
            f"{self.ficha_origen.codigo_ficha} → "
            f"{self.ficha_destino.codigo_ficha}"
        )

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.ficha_origen == self.ficha_destino:
            raise ValidationError(
                'La ficha de origen y destino no pueden ser la misma.'
            )