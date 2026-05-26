from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from docentes.models.docente import Docente
from docentes.serializers import DocenteListSerializer
from docentes.filters.docente_filter import DocenteFilter, DocentePagination
from users.permissions import IsManager
from docentes.views.base_view_docente import DocenteBaseView


class DocenteListView(DocenteBaseView):
    """
    GET /api/docentes/
    Solo COORDINADOR y ADMINISTRATIVO.
    Soporta búsqueda, filtro por estado/especialidad y paginación.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        queryset = Docente.objects.select_related('user').order_by('user__nombre')

        filterset = DocenteFilter(request.GET, queryset=queryset, request=request)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)

        paginator = DocentePagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        serializer = DocenteListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)