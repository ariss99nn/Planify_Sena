from django.db import models
from django.conf import settings
from programa.models.modulo import Modulo


class DocenteModulo(models.Model):
    """
    Docente habilitado para un modulo completo.
    Complementa DocenteAsignatura (granularidad por asignatura).
    """
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='modulos_asignados',
        limit_choices_to={'rol': 'DOCENTE'},
    )
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.PROTECT,
        related_name='docentes_asignados',
    )
    fecha_asignacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Docente por modulo'
        verbose_name_plural = 'Docentes por modulo'
        unique_together = [('docente', 'modulo')]
        ordering = ['modulo', 'docente']

    def __str__(self):
        return f"{self.docente.nombre} -> {self.modulo.nombre}"