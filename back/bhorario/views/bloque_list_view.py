from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bhorario.models.bloque_horario_model import BloqueHorario
from bhorario.serializers import BloqueHorarioListSerializer
from bhorario.filters import BloqueHorarioFilter, BhorarioPagination
from bhorario.views.base import BhorarioBaseView
from users.models.user import User


class BloqueHorarioListView(BhorarioBaseView):
    """
    GET /api/horarios/
    - IsManager: todos los bloques.
    - DOCENTE: solo sus bloques asignados.
    - ESTUDIANTE: bloques de su ficha activa.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        qs = BloqueHorario.objects.select_related(
            'aula', 'docente__user', 'ficha__version__programa'
        )

        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            return qs

        if user.rol == User.Rol.DOCENTE:
            return qs.filter(docente__user=user)

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_estudiante_model import FichaEstudiante
            ficha_ids = FichaEstudiante.objects.filter(
                estudiante=user, activo=True
            ).values_list('ficha_id', flat=True)
            return qs.filter(ficha_id__in=ficha_ids)

        return qs.none()

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = BloqueHorarioFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = BhorarioPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            BloqueHorarioListSerializer(page, many=True).data
        )