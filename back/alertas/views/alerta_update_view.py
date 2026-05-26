from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from alertas.serializers import AlertaUpdateSerializer, AlertaListSerializer
from alertas.views.base import AlertaBaseView
from users.models.user import User


class AlertaUpdateView(AlertaBaseView):
    """
    PATCH /api/alertas/{id}/update/
    - IsManager: puede cambiar cualquier estado.
    - DOCENTE/ESTUDIANTE: solo pueden marcar sus propias alertas como LEIDA.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        alerta, error = self.get_alerta_or_404(pk)
        if error:
            return error

        user = request.user
        if user.rol not in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            if alerta.destinatario != user:
                return Response(
                    {'detail': 'No tienes acceso a esta alerta.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = AlertaUpdateSerializer(
            alerta, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AlertaListSerializer(alerta).data)