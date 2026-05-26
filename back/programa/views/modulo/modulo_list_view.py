from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.models.modulo import Modulo
from programa.serializers import ModuloListSerializer
from programa.filters import ModuloFilter, ProgramaPagination
from programa.views.base import ProgramaBaseView
from users.models.user import User


class ModuloListView(ProgramaBaseView):
    """
    GET /api/modulos/
    ESTUDIANTE: solo módulos de la versión de su ficha activa.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        qs = Modulo.objects.select_related('version__programa')

        if request.user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_model import Ficha
            version_ids = Ficha.objects.filter(
                estado=True,
            ).values_list('version_id', flat=True).distinct()
            return qs.filter(version_id__in=version_ids)

        return qs

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = ModuloFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = ProgramaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            ModuloListSerializer(page, many=True).data
        )