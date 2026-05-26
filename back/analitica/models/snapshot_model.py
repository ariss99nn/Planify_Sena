# analitica/models.py
from django.db import models


class AnalíticaSnapshot(models.Model):
    """
    Snapshot diario de metricas del sistema.
    Generado por Celery Beat cada noche.
    Permite dashboards rapidos sin queries complejas en tiempo real.
    Sin cambios de fondo; documentacion mejorada.
    """
    fecha = models.DateField(db_index=True, unique=True)  # CORRECCION: unique=True

    fichas_activas    = models.PositiveIntegerField(default=0)
    fichas_lectiva    = models.PositiveIntegerField(default=0)
    fichas_productiva = models.PositiveIntegerField(default=0)

    estudiantes_activos  = models.PositiveIntegerField(default=0)
    deserciones_mes      = models.PositiveIntegerField(default=0)
    graduados_mes        = models.PositiveIntegerField(default=0)
    reasignaciones_mes   = models.PositiveIntegerField(default=0)

    docentes_activos      = models.PositiveIntegerField(default=0)
    docentes_sobrecargados = models.PositiveIntegerField(
        default=0,
        help_text='Docentes con mas horas que su maximo semanal x 12.',
    )

    aulas_activas       = models.PositiveIntegerField(default=0)
    aulas_mantenimiento = models.PositiveIntegerField(default=0)
    aulas_inactivas     = models.PositiveIntegerField(default=0)

    planes_aprobados  = models.PositiveIntegerField(default=0)
    planes_pendientes = models.PositiveIntegerField(default=0)

    alertas_pendientes      = models.PositiveIntegerField(default=0)
    conflictos_horario_mes  = models.PositiveIntegerField(default=0)

    # JSON: lista de {programa, fichas, estudiantes}
    breakdown_programas = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Snapshot de analitica'
        verbose_name_plural = 'Snapshots de analitica'
        ordering = ['-fecha']
        get_latest_by = 'fecha'

    def __str__(self):
        return f"Snapshot {self.fecha}"