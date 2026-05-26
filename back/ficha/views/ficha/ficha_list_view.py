from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ficha.models.ficha_model import Ficha
from ficha.serializers import FichaListSerializer
from ficha.filter.filter import FichaFilter, FichaPagination
from ficha.views.base import FichaBaseView
from users.models.user import User


class FichaListView(FichaBaseView):
    """
    GET /api/fichas/
    - IsManager: todas las fichas.
    - DOCENTE: fichas donde es jefe de grupo.
    - ESTUDIANTE: solo su ficha activa.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        qs = Ficha.objects.select_related(
            'version__programa', 'jefe_grupo'
        )

        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            return qs

        if user.rol == User.Rol.DOCENTE:
            return qs.filter(jefe_grupo=user)

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_estudiante_model import FichaEstudiante
            ficha_ids = FichaEstudiante.objects.filter(
                estudiante=user,
                activo=True,
            ).values_list('ficha_id', flat=True)
            return qs.filter(pk__in=ficha_ids)

        return qs.none()

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = FichaFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = FichaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            FichaListSerializer(page, many=True).data
        )