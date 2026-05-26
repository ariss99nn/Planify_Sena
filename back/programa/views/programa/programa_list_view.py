from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.models.programa_model import Programa
from programa.serializers import ProgramaListSerializer
from programa.filters import ProgramaFilter, ProgramaPagination
from programa.views.base import ProgramaBaseView
from users.models.user import User


class ProgramaListView(ProgramaBaseView):
    """
    GET /api/programas/
    - IsManager y DOCENTE: todos los programas.
    - ESTUDIANTE: solo el programa de su ficha activa.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN, User.Rol.DOCENTE}:
            return Programa.objects.all()

        if user.rol == User.Rol.ESTUDIANTE:
            # Solo el programa de su ficha activa
            # La relación: ficha → version → programa
            from ficha.models.ficha_model import Ficha
            fichas = Ficha.objects.filter(
                estado=True,
            ).select_related('version__programa')
            programa_ids = fichas.values_list(
                'version__programa_id', flat=True
            ).distinct()
            return Programa.objects.filter(pk__in=programa_ids)

        return Programa.objects.none()

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = ProgramaFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = ProgramaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            ProgramaListSerializer(page, many=True).data
        )