from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ficha.models.reasignacion_ficha_model import ReasignacionFicha
from ficha.serializers import ReasignacionListSerializer
from ficha.filter.filter import FichaPagination
from users.permissions import IsManager
from ficha.views.base import FichaBaseView


class ReasignacionListView(FichaBaseView):
    """GET /api/fichas/reasignaciones/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        queryset = ReasignacionFicha.objects.select_related(
            'estudiante',
            'ficha_origen__version__programa',
            'ficha_destino__version__programa',
            'realizado_por',
        )

        estudiante_id = request.query_params.get('estudiante')
        ficha_origen_id = request.query_params.get('ficha_origen')
        ficha_destino_id = request.query_params.get('ficha_destino')

        if estudiante_id:
            queryset = queryset.filter(estudiante_id=estudiante_id)
        if ficha_origen_id:
            queryset = queryset.filter(ficha_origen_id=ficha_origen_id)
        if ficha_destino_id:
            queryset = queryset.filter(ficha_destino_id=ficha_destino_id)

        paginator = FichaPagination()
        page = paginator.paginate_queryset(queryset, request)
        return paginator.get_paginated_response(
            ReasignacionListSerializer(page, many=True).data
        )