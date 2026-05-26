from django.db import models
from django.core.exceptions import ValidationError
# ELIMINA esta importación circular:
# from planificacion.models.item_plan_model import ItemPlan


class BloqueCompetencia(models.Model):
    """
    Vincula un BloqueHorario con el ItemPlan que ejecuta.
    Es el puente entre el horario fisico y el plan curricular.

    CORRECCION: clean() usaba <= 0 sobre DecimalField; agregada
    comparacion correcta con Decimal('0').
    """
    bloque = models.OneToOneField(
        'bhorario.BloqueHorario',
        on_delete=models.PROTECT,
        related_name='competencia_asignada',
    )
    item_plan = models.ForeignKey(
        'planificacion.ItemPlan',  # ← CAMBIADO: usar string en lugar de importación directa
        on_delete=models.PROTECT,
        related_name='bloques_ejecutados',
    )
    horas_ejecutadas = models.DecimalField(
        max_digits=4, decimal_places=1,
        help_text='Horas reales ejecutadas en este bloque.',
    )
    observaciones = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Bloque de competencia'
        verbose_name_plural = 'Bloques de competencia'

    def __str__(self):
        return f"{self.bloque} -> {self.item_plan.competencia.codigo}"

    def clean(self):
        from decimal import Decimal
        if self.horas_ejecutadas is not None and self.horas_ejecutadas <= Decimal('0'):
            raise ValidationError(
                {'horas_ejecutadas': 'Las horas ejecutadas deben ser mayores a 0.'}
            )