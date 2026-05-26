from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from alertas.models.alerta_model import Alerta
from alertas.serializers import AlertaListSerializer
from alertas.filters import AlertaFilter, AlertaPagination
from alertas.views.base import AlertaBaseView
from users.models.user import User


class AlertaListView(AlertaBaseView):
    """
    GET /api/alertas/
    - IsManager: todas las alertas.
    - DOCENTE/ESTUDIANTE: solo sus propias alertas.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        qs = Alerta.objects.select_related('bloque_origen', 'destinatario')

        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            return qs

        return qs.filter(destinatario=user)

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = AlertaFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = AlertaPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            AlertaListSerializer(page, many=True).data
        )