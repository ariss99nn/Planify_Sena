from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
# ELIMINA esta importación circular:
# from planificacion.models.bloque_competencia_model import BloqueCompetencia


class PlanTrimestral(models.Model):
    """
    Planificacion curricular de una ficha para un trimestre.
    Solo los planes aprobados permiten generar BloqueHorario.
    """
    ficha = models.ForeignKey(
        'ficha.Ficha',
        on_delete=models.PROTECT,
        related_name='planes_trimestrales',
    )
    trimestre = models.PositiveIntegerField(
        help_text='Numero de trimestre al que aplica este plan.',
    )
    fecha_inicio = models.DateField()
    fecha_fin    = models.DateField()
    aprobado = models.BooleanField(
        default=False, db_index=True,
        help_text='Solo planes aprobados permiten generar horarios.',
    )
    aprobado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='planes_aprobados',
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Plan trimestral'
        verbose_name_plural = 'Planes trimestrales'
        unique_together = [('ficha', 'trimestre')]
        ordering = ['ficha', 'trimestre']

    def __str__(self):
        return f"Ficha {self.ficha.codigo_ficha} -- Trimestre {self.trimestre}"

    def clean(self):
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin <= self.fecha_inicio:
            raise ValidationError(
                {'fecha_fin': 'La fecha de fin debe ser posterior a la de inicio.'}
            )
        if self.ficha_id:
            trimestres_max = getattr(
                self.ficha.version.programa, 'trimestres_totales', None
            )
            if trimestres_max and self.trimestre > trimestres_max:
                raise ValidationError({
                    'trimestre': (
                        f'El trimestre no puede superar {trimestres_max} '
                        f'para este programa.'
                    )
                })

    @property
    def total_horas_planificadas(self):
        return sum(item.horas_asignadas for item in self.items.all())

    @property
    def total_horas_ejecutadas(self):
        from django.db.models import Sum
        # Usar apps.get_model() para evitar importación circular
        from django.apps import apps
        BloqueCompetencia = apps.get_model('planificacion', 'BloqueCompetencia')
        result = BloqueCompetencia.objects.filter(
            item_plan__plan=self
        ).aggregate(total=Sum('horas_ejecutadas'))
        return result['total'] or 0

    @property
    def porcentaje_avance(self):
        total = self.total_horas_planificadas
        if not total:
            return 0
        return round((self.total_horas_ejecutadas / total) * 100, 1)