from django.db import models
from django.conf import settings
from ficha.models.ficha_model import Ficha


class HistorialEtapa(models.Model):
    """
    Registro inmutable de cada cambio de etapa en una ficha.
    Se crea automáticamente al cambiar Ficha.etapa.
    Nunca se edita ni se elimina — es auditoría pura.
    """

    ficha = models.ForeignKey(
        Ficha,
        on_delete=models.PROTECT,
        related_name='historial_etapas',
    )
    etapa_anterior = models.CharField(
        max_length=15,
        choices=Ficha.Etapa.choices,
    )
    etapa_nueva = models.CharField(
        max_length=15,
        choices=Ficha.Etapa.choices,
    )
    trimestre = models.PositiveIntegerField(
        help_text='Trimestre en el momento del cambio.',
    )
    fecha = models.DateTimeField(auto_now_add=True)
    cambiado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cambios_etapa',
        null=True,
        blank=True,
        help_text='Usuario que realizó el cambio.',
    )

    class Meta:
        verbose_name = 'Historial de etapa'
        verbose_name_plural = 'Historial de etapas'
        ordering = ['ficha', '-fecha']

    def __str__(self):
        return (
            f"Ficha {self.ficha.codigo_ficha}: "
            f"{self.etapa_anterior} → {self.etapa_nueva} "
            f"({self.fecha.date()})"
        )