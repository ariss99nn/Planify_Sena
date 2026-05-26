from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.models.aula import Aula
from aulas.serializers import AulaListSerializer
from aulas.filters.aula_filter import AulaFilter, AulaPagination
from aulas.views.base_view import AulaBaseView


class AulaListView(AulaBaseView):
    """GET /api/aulas/ — todos los roles autenticados."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Aula.objects.select_related('bloque').all()
        filterset = AulaFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = AulaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            AulaListSerializer(page, many=True).data
        )