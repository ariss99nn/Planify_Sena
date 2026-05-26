from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsManager


class DashboardView(APIView):
    """
    GET /api/dashboard/
    Retorna el último snapshot + datos en tiempo real críticos.
    Diseñado para ser rápido — la mayor parte viene del snapshot pre-agregado.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        from analitica.models.snapshot_model import AnalíticaSnapshot
        from alertas.models.alerta_model import Alerta

        try:
            snapshot = AnalíticaSnapshot.objects.latest()
            data = {
                'fecha_snapshot': snapshot.fecha,
                'fichas': {
                    'activas': snapshot.fichas_activas,
                    'lectiva': snapshot.fichas_lectiva,
                    'productiva': snapshot.fichas_productiva,
                },
                'estudiantes': {
                    'activos': snapshot.estudiantes_activos,
                    'deserciones_mes': snapshot.deserciones_mes,
                    'graduados_mes': snapshot.graduados_mes,
                    'reasignaciones_mes': snapshot.reasignaciones_mes,
                },
                'docentes': {
                    'activos': snapshot.docentes_activos,
                    'sobrecargados': snapshot.docentes_sobrecargados,
                },
                'aulas': {
                    'activas': snapshot.aulas_activas,
                    'mantenimiento': snapshot.aulas_mantenimiento,
                    'inactivas': snapshot.aulas_inactivas,
                },
                'planes': {
                    'aprobados': snapshot.planes_aprobados,
                    'pendientes': snapshot.planes_pendientes,
                },
                'alertas': {
                    'pendientes': snapshot.alertas_pendientes,
                    'conflictos_mes': snapshot.conflictos_horario_mes,
                },
                'breakdown_programas': snapshot.breakdown_programas,
                # Alertas en tiempo real — siempre frescos
                'alertas_criticas': list(
                    Alerta.objects.filter(
                        estado=Alerta.EstadoAlerta.PENDIENTE,
                        tipo=Alerta.TipoAlerta.CONFLICTO,
                    ).values(
                        'id', 'descripcion', 'fecha_creacion'
                    ).order_by('-fecha_creacion')[:5]
                ),
            }
        except AnalíticaSnapshot.DoesNotExist:
            data = {'mensaje': 'No hay snapshots generados aún. Ejecuta la tarea Celery.'}

        return Response(data)