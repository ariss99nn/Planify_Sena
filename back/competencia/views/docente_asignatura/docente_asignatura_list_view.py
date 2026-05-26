from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.models.docente_asignatura_model import DocenteAsignatura
from competencia.serializers import DocenteAsignaturaListSerializer
from competencia.filters import CompetenciaPagination
from competencia.views.base import CompetenciaBaseView
from users.permissions import IsManager
from users.models.user import User


class DocenteAsignaturaListView(CompetenciaBaseView):
    """
    IsManager: ve todas las asignaciones.
    DOCENTE: ve solo sus propias asignaciones.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        qs = DocenteAsignatura.objects.select_related('docente', 'asignatura')

        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            asignatura_id = request.query_params.get('asignatura')
            docente_id = request.query_params.get('docente')
            activo = request.query_params.get('activo')
            if asignatura_id:
                qs = qs.filter(asignatura_id=asignatura_id)
            if docente_id:
                qs = qs.filter(docente_id=docente_id)
            if activo is not None:
                qs = qs.filter(activo=activo.lower() == 'true')
            return qs

        if user.rol == User.Rol.DOCENTE:
            return qs.filter(docente=user)

        return qs.none()

    def get(self, request):
        queryset = self.get_queryset(request)
        paginator = CompetenciaPagination()
        page = paginator.paginate_queryset(queryset, request)
        return paginator.get_paginated_response(
            DocenteAsignaturaListSerializer(page, many=True).data
        )