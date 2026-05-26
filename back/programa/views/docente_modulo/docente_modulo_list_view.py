from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.models.docente_modulo_model import DocenteModulo
from programa.serializers import DocenteModuloListSerializer
from programa.filters import ProgramaPagination
from users.permissions import IsManager
from programa.views.base import ProgramaBaseView


class DocenteModuloListView(ProgramaBaseView):
    """GET /api/docentes-modulo/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        queryset = DocenteModulo.objects.select_related(
            'docente', 'modulo'
        ).all()

        # Filtros opcionales por query params
        modulo_id = request.query_params.get('modulo')
        docente_id = request.query_params.get('docente')
        activo = request.query_params.get('activo')

        if modulo_id:
            queryset = queryset.filter(modulo_id=modulo_id)
        if docente_id:
            queryset = queryset.filter(docente_id=docente_id)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')

        paginator = ProgramaPagination()
        page = paginator.paginate_queryset(queryset, request)
        return paginator.get_paginated_response(
            DocenteModuloListSerializer(page, many=True).data
        )