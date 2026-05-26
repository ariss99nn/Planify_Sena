# reportes/tasks.py
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generar_reporte(self, tipo: str, filtros: dict, usuario_id: int):
    """
    Genera un reporte de forma asíncrona.
    El frontend puede consultar el estado via GET /api/reportes/{id}/
    """
    from reportes.models.reporte_generado import ReporteGenerado
    from reportes.services.reporte_factory import ReporteFactory
    from django.core.files.base import ContentFile

    reporte = ReporteGenerado.objects.create(
        tipo=tipo,
        estado=ReporteGenerado.EstadoReporte.PROCESANDO,
        filtros=filtros,
        usuario_id=usuario_id,
        tarea_id=self.request.id,
    )

    try:
        generador = ReporteFactory.crear(tipo, filtros)

        pdf = generador.generar_pdf()
        reporte.archivo_pdf.save(
            f'{tipo}_{self.request.id}.pdf',
            ContentFile(pdf),
            save=False,
        )

        excel = generador.generar_excel()
        reporte.archivo_excel.save(
            f'{tipo}_{self.request.id}.xlsx',
            ContentFile(excel),
            save=False,
        )

        reporte.estado = ReporteGenerado.EstadoReporte.LISTO
        reporte.save(update_fields=['estado', 'archivo_pdf', 'archivo_excel'])

        logger.info("Reporte %s generado — id=%s", tipo, reporte.pk)
        return {'estado': 'listo', 'reporte_id': reporte.pk}

    except Exception as exc:
        reporte.estado = ReporteGenerado.EstadoReporte.ERROR
        reporte.error_mensaje = str(exc)
        reporte.save(update_fields=['estado', 'error_mensaje'])
        logger.error("Error generando reporte %s: %s", tipo, str(exc))
        raise self.retry(exc=exc)


@shared_task
def limpiar_reportes_antiguos(dias: int = 30):
    """Elimina reportes y archivos generados hace más de N días."""
    from django.utils import timezone
    from datetime import timedelta
    from reportes.models.reporte_generado import ReporteGenerado

    limite = timezone.now() - timedelta(days=dias)
    reportes = ReporteGenerado.objects.filter(created_at__lt=limite)
    for reporte in reportes:
        if reporte.archivo_pdf:
            reporte.archivo_pdf.delete(save=False)
        if reporte.archivo_excel:
            reporte.archivo_excel.delete(save=False)
    count = reportes.count()
    reportes.delete()
    logger.info("Reportes eliminados: %s", count)