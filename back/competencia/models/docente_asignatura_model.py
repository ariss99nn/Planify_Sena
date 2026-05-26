# competencia/models/docente_asignatura_model.py
from django.db import models
from competencia.models.asignatura_model import Asignatura


class DocenteAsignatura(models.Model):
    """
    Asignación de un docente (perfil Docente) a una asignatura específica.
    Diferencia con DocenteModulo: este es granular (asignatura por asignatura).
    Úsalo cuando un docente cubre solo algunas asignaturas del módulo.
    DocenteModulo se usa cuando cubre el módulo completo.
    """

    # CORRECCIÓN: FK a Docente (perfil extendido), NO a AUTH_USER_MODEL directamente.
    # Esto garantiza que solo usuarios con perfil de docente pueden asignarse.
    docente = models.ForeignKey(
        'docentes.Docente',
        on_delete=models.PROTECT,
        related_name='asignaturas_asignadas',
    )
    asignatura = models.ForeignKey(
        Asignatura,
        on_delete=models.PROTECT,
        related_name='docentes_asignados',
    )
    fecha_asignacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Docente por asignatura'
        verbose_name_plural = 'Docentes por asignatura'
        unique_together     = [('docente', 'asignatura')]
        ordering            = ['asignatura', 'docente']

    def __str__(self):
        return f"{self.docente.user.nombre} → {self.asignatura.nombre}"