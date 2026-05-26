from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.models.asignatura_model import Asignatura
from competencia.serializers import AsignaturaListSerializer
from competencia.filters import AsignaturaFilter, CompetenciaPagination
from competencia.views.base import CompetenciaBaseView
from users.models.user import User


class AsignaturaListView(CompetenciaBaseView):
    """
    GET /api/asignaturas/
    - IsManager y DOCENTE (solo sus asignaturas asignadas activas).
    - ESTUDIANTE: asignaturas del módulo de su ficha activa.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        qs = Asignatura.objects.select_related('modulo')

        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            return qs

        if user.rol == User.Rol.DOCENTE:
            from competencia.models.docente_asignatura_model import DocenteAsignatura
            asignatura_ids = DocenteAsignatura.objects.filter(
                docente=user, activo=True
            ).values_list('asignatura_id', flat=True)
            return qs.filter(pk__in=asignatura_ids)

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_model import Ficha
            modulo_ids = Ficha.objects.filter(
                estado=True,
            ).values_list(
                'version__modulos__id', flat=True
            ).distinct()
            return qs.filter(modulo_id__in=modulo_ids)

        return qs.none()

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = AsignaturaFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = CompetenciaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            AsignaturaListSerializer(page, many=True).data
        )