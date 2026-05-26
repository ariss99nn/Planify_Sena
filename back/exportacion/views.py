from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from exportacion.serializers import ExportacionRequestSerializer
from exportacion.services.exportacion_service import ExportacionService
from users.permissions import IsManager


class ExportarView(APIView):
    """
    POST /api/exportar/
    Exporta datos en CSV o Excel directamente (sin Celery).
    Para reportes grandes o con gráficas usar /api/reportes/solicitar/.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = ExportacionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        modulo = serializer.validated_data['modulo']
        formato = serializer.validated_data['formato']
        filtros = serializer.validated_data.get('filtros', {})

        try:
            headers, rows = ExportacionService.exportar(modulo, filtros, formato)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if formato == 'csv':
            contenido = ExportacionService.a_csv(headers, rows)
            response = HttpResponse(contenido, content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = (
                f'attachment; filename="{modulo}.csv"'
            )
        else:
            contenido = ExportacionService.a_excel(headers, rows)
            response = HttpResponse(
                contenido,
                content_type=(
                    'application/vnd.openxmlformats-officedocument'
                    '.spreadsheetml.sheet'
                ),
            )
            response['Content-Disposition'] = (
                f'attachment; filename="{modulo}.xlsx"'
            )

        return response