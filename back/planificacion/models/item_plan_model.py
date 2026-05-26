from django.db import models
from django.core.exceptions import ValidationError

class ItemPlan(models.Model):
    """
    Cada competencia dentro de un PlanTrimestral.
    Puede ser principal (asignatura del programa) o transversal.
    """
    plan = models.ForeignKey(
    'planificacion.PlanTrimestral',  # ← string
    on_delete=models.PROTECT,
    related_name='items',
)
    competencia = models.ForeignKey(
        'competencia.Competencia',
        on_delete=models.PROTECT,
        related_name='items_plan',
    )
    docente = models.ForeignKey(
        'docentes.Docente',
        on_delete=models.PROTECT,
        related_name='items_plan',
        null=True, blank=True,
        help_text='Docente asignado a esta competencia en este trimestre.',
    )
    horas_asignadas = models.PositiveIntegerField(
        help_text='Horas totales planificadas para esta competencia.',
    )
    orden = models.PositiveIntegerField(
        help_text='Orden de dictado dentro del trimestre.',
    )
    completado = models.BooleanField(default=False)

    class Meta:
        verbose_name        = 'Item de plan'
        verbose_name_plural = 'Items de plan'
        unique_together = [('plan', 'competencia')]
        ordering = ['plan', 'orden']

    def __str__(self):
        return f"{self.plan} -- {self.competencia.codigo} ({self.horas_asignadas}h)"

    def clean(self):
        if self.horas_asignadas <= 0:
            raise ValidationError(
                {'horas_asignadas': 'Las horas asignadas deben ser mayores a 0.'}
            )
        if self.competencia_id and self.competencia.asignatura_id:
            asignatura = self.competencia.asignatura
            horas_max = asignatura.total_horas
            if self.horas_asignadas > horas_max:
                raise ValidationError({
                    'horas_asignadas': (
                        f'No puede superar las {horas_max}h '
                        f'de la asignatura "{asignatura.nombre}".'
                    )
                })

    @property
    def horas_ejecutadas(self):
        from django.db.models import Sum
        result = self.bloques_ejecutados.aggregate(total=Sum('horas_ejecutadas'))
        return result['total'] or 0

    @property
    def horas_restantes(self):
        return max(0, self.horas_asignadas - self.horas_ejecutadas)

    @property
    def porcentaje_avance(self):
        if not self.horas_asignadas:
            return 0
        return round((self.horas_ejecutadas / self.horas_asignadas) * 100, 1)