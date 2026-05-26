from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.models.version_programa_model import VersionPrograma
from programa.serializers import VersionListSerializer
from programa.filters import VersionFilter, ProgramaPagination
from programa.views.base import ProgramaBaseView
from users.models.user import User


class VersionListView(ProgramaBaseView):
    """
    GET /api/versiones/
    ESTUDIANTE: solo versiones del programa de su ficha activa.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        qs = VersionPrograma.objects.select_related('programa')

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_model import Ficha
            version_ids = Ficha.objects.filter(
                estado=True,
            ).values_list('version_id', flat=True).distinct()
            return qs.filter(pk__in=version_ids)

        return qs

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = VersionFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = ProgramaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            VersionListSerializer(page, many=True).data
        )