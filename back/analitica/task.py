from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def generar_snapshot_diario():
    """Genera el snapshot de analítica del día. Ejecutar via Celery Beat."""
    from django.utils import timezone
    from django.db.models import Count, Q
    from analitica.models.snapshot_model import AnalíticaSnapshot
    from ficha.models.ficha_model import Ficha
    from ficha.models.ficha_estudiante_model import FichaEstudiante
    from docentes.models.docente import Docente
    from aulas.models.aula import Aula
    from planificacion.models.plan_trimestral_model import PlanTrimestral
    from alertas.models.alerta_model import Alerta
    from programa.models.programa_model import Programa

    hoy = timezone.now().date()
    mes_actual = timezone.now().replace(day=1).date()

    fichas_activas = Ficha.objects.filter(estado=True)

    breakdown = []
    for programa in Programa.objects.filter(estado=Programa.Estado.ACTIVO):
        fichas_prog = fichas_activas.filter(
            version__programa=programa
        )
        estudiantes_prog = FichaEstudiante.objects.filter(
            ficha__in=fichas_prog, activo=True
        ).count()
        breakdown.append({
            'programa': programa.nombre,
            'nivel': programa.get_nivel_display(),
            'fichas': fichas_prog.count(),
            'estudiantes': estudiantes_prog,
        })

    snapshot = AnalíticaSnapshot.objects.create(
        fecha=hoy,
        fichas_activas=fichas_activas.count(),
        fichas_lectiva=fichas_activas.filter(
            etapa=Ficha.Etapa.LECTIVA
        ).count(),
        fichas_productiva=fichas_activas.filter(
            etapa=Ficha.Etapa.PRODUCTIVA
        ).count(),
        estudiantes_activos=FichaEstudiante.objects.filter(
            activo=True
        ).count(),
        deserciones_mes=FichaEstudiante.objects.filter(
            activo=False,
            motivo_retiro='DESERCION',
            fecha_retiro__gte=mes_actual,
        ).count(),
        graduados_mes=FichaEstudiante.objects.filter(
            activo=False,
            motivo_retiro='GRADUADO',
            fecha_retiro__gte=mes_actual,
        ).count(),
        reasignaciones_mes=FichaEstudiante.objects.filter(
            activo=False,
            motivo_retiro='REASIGNADO',
            fecha_retiro__gte=mes_actual,
        ).count(),
        docentes_activos=Docente.objects.filter(estado=True).count(),
        aulas_activas=Aula.objects.filter(estado=Aula.Estado.ACTIVA).count(),
        aulas_mantenimiento=Aula.objects.filter(
            estado=Aula.Estado.MANTENIMIENTO
        ).count(),
        aulas_inactivas=Aula.objects.filter(
            estado=Aula.Estado.INACTIVA
        ).count(),
        planes_aprobados=PlanTrimestral.objects.filter(aprobado=True).count(),
        planes_pendientes=PlanTrimestral.objects.filter(aprobado=False).count(),
        alertas_pendientes=Alerta.objects.filter(
            estado=Alerta.EstadoAlerta.PENDIENTE
        ).count(),
        conflictos_horario_mes=Alerta.objects.filter(
            tipo=Alerta.TipoAlerta.CONFLICTO,
            fecha_creacion__date__gte=mes_actual,
        ).count(),
        breakdown_programas=breakdown,
    )
    logger.info("Snapshot generado: %s", hoy)
    return snapshot.pk


# En settings.py agregar Celery Beat:
# CELERY_BEAT_SCHEDULE = {
#     'snapshot-diario': {
#         'task': 'analitica.tasks.generar_snapshot_diario',
#         'schedule': crontab(hour=2, minute=0),  # 2 AM cada noche
#     },
#     'limpiar-reportes': {
#         'task': 'reportes.tasks.limpiar_reportes_antiguos',
#         'schedule': crontab(hour=3, minute=0),
#     },
# }