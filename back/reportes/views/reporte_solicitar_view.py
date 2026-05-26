from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsManager
from reportes.tasks import generar_reporte
from reportes.models.reporte_generado import ReporteGenerado


class SolicitarReporteView(APIView):
    """
    POST /api/reportes/solicitar/
    Encola la generación del reporte y retorna el ID para consultar estado.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        tipo = request.data.get('tipo')
        filtros = request.data.get('filtros', {})

        tipos_validos = [c[0] for c in ReporteGenerado.TipoReporte.choices]
        if tipo not in tipos_validos:
            return Response(
                {'detail': f'Tipo inválido. Opciones: {tipos_validos}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task = generar_reporte.delay(
            tipo=tipo,
            filtros=filtros,
            usuario_id=request.user.pk,
        )
        return Response(
            {'task_id': task.id, 'estado': 'procesando'},
            status=status.HTTP_202_ACCEPTED,
        )


class EstadoReporteView(APIView):
    """GET /api/reportes/{id}/ — consulta estado del reporte."""
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, pk):
        try:
            reporte = ReporteGenerado.objects.get(
                pk=pk, usuario=request.user
            )
        except ReporteGenerado.DoesNotExist:
            return Response(
                {'detail': 'Reporte no encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = {
            'id': reporte.pk,
            'tipo': reporte.tipo,
            'estado': reporte.estado,
            'created_at': reporte.created_at,
            'error': reporte.error_mensaje or None,
            'pdf_url': reporte.archivo_pdf.url if reporte.archivo_pdf else None,
            'excel_url': reporte.archivo_excel.url if reporte.archivo_excel else None,
        }
        return Response(data)