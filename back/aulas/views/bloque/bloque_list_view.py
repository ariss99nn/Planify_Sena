from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.models.bloque import Bloque
from aulas.serializers import BloqueListSerializer
from aulas.filters.aula_filter import BloqueFilter, AulaPagination
from aulas.views.base_view import AulaBaseView

# CORRECCIÓN: eliminado 'from django_filters.rest_framework import DjangoFilterBackend'
# DjangoFilterBackend solo aplica con GenericAPIView/ViewSet. En APIView el filtrado
# se hace instanciando el FilterSet directamente, como ya hace este código.
# El import era un dead import que no hacía nada.


class BloqueListView(AulaBaseView):
    """GET /api/aulas/bloques/ — todos los roles autenticados."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Bloque.objects.all()
        filterset = BloqueFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = AulaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            BloqueListSerializer(page, many=True).data
        )