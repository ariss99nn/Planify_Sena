from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from ficha.models.ficha_model import Ficha


class FichaEstudiante(models.Model):

    class MotivoRetiro(models.TextChoices):
        DESERCION = 'DESERCION', 'Deserción'
        RETIRO_VOLUNTARIO = 'RETIRO_VOLUNTARIO', 'Retiro voluntario'
        CANCELADO = 'CANCELADO', 'Cancelado por rendimiento'
        GRADUADO = 'GRADUADO', 'Graduado'
        REASIGNADO = 'REASIGNADO', 'Reasignado a otra ficha'

    ficha = models.ForeignKey(
        Ficha,
        on_delete=models.PROTECT,
        related_name='estudiantes',
    )
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='fichas_asignadas',
        limit_choices_to={'rol': 'ESTUDIANTE'},
    )
    activo = models.BooleanField(default=True, db_index=True)
    es_cadena = models.BooleanField(
        default=False,
        help_text=(
            'True si el estudiante ingresó por cadena de formación '
            '(reduce tiempo en etapa lectiva).'
        ),
    )
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_retiro = models.DateField(
        null=True,
        blank=True,
    )
    motivo_retiro = models.CharField(
        max_length=20,
        choices=MotivoRetiro.choices,
        null=True,
        blank=True,
        db_index=True,
        help_text='Obligatorio al desactivar al estudiante.',
    )

    class Meta:
        verbose_name = 'Estudiante en ficha'
        verbose_name_plural = 'Estudiantes en ficha'
        unique_together = [('ficha', 'estudiante')]
        ordering = ['ficha', 'estudiante__nombre']
        indexes = [
            models.Index(fields=['activo']),
            models.Index(fields=['es_cadena']),
            models.Index(fields=['motivo_retiro']),
        ]

    def __str__(self):
        return f"{self.estudiante.nombre} → Ficha {self.ficha.codigo_ficha}"

    def clean(self):
        # Validar unicidad de ficha activa para no-cadena
        if not self.es_cadena and self.activo:
            activas = FichaEstudiante.objects.filter(
                estudiante=self.estudiante,
                activo=True,
                es_cadena=False,
            ).exclude(pk=self.pk)
            if activas.exists():
                raise ValidationError(
                    'Este estudiante ya tiene una ficha activa. '
                    'Usa reasignación para cambiarlo de ficha, '
                    'o marca como cadena de formación si aplica.'
                )

        # Al desactivar, fecha_retiro y motivo_retiro son obligatorios
        if not self.activo:
            if not self.fecha_retiro:
                raise ValidationError({
                    'fecha_retiro': 'La fecha de retiro es obligatoria al desactivar.'
                })
            if not self.motivo_retiro:
                raise ValidationError({
                    'motivo_retiro': 'El motivo de retiro es obligatorio al desactivar.'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)