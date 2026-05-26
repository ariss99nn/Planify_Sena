from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.models.resultado_aprendizaje_model import ResultadoAprendizaje
from competencia.serializers import RAPListSerializer
from competencia.filters import RAPFilter, CompetenciaPagination
from competencia.views.base import CompetenciaBaseView
from users.models.user import User


class RAPListView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        qs = ResultadoAprendizaje.objects.select_related(
            'competencia__asignatura'
        )

        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            return qs

        if user.rol == User.Rol.DOCENTE:
            from competencia.models.docente_asignatura_model import DocenteAsignatura
            asignatura_ids = DocenteAsignatura.objects.filter(
                docente=user, activo=True
            ).values_list('asignatura_id', flat=True)
            return qs.filter(
                competencia__asignatura_id__in=asignatura_ids
            )

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_model import Ficha
            modulo_ids = Ficha.objects.filter(
                estado=True,
            ).values_list('version__modulos__id', flat=True).distinct()
            return qs.filter(
                competencia__asignatura__modulo_id__in=modulo_ids
            )

        return qs.none()

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = RAPFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = CompetenciaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            RAPListSerializer(page, many=True).data
        )