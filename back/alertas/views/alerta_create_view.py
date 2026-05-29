from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from alertas.models.alerta_model import Alerta
from alertas.serializers import AlertaCreateSerializer, AlertaListSerializer
from alertas.views.base import AlertaBaseView
from users.models.user import User
from users.permissions import IsManager


class AlertaCreateView(AlertaBaseView):
    """
    POST /api/alertas/create/

    Casos:
      - destinatario presente  → crea 1 alerta.
      - destinatario_rol       → crea N alertas (bulk) para todos los
                                 usuarios activos de ese rol.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = AlertaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data     = serializer.validated_data
        rol      = data.pop('destinatario_rol', None)
        individual = data.get('destinatario')

        if individual:
            alerta = Alerta.objects.create(**data)
            return Response(
                AlertaListSerializer(alerta).data,
                status=status.HTTP_201_CREATED,
            )

        # Envío masivo por rol
        usuarios = User.objects.filter(rol=rol, is_active=True)
        if not usuarios.exists():
            return Response(
                {'detail': f'No hay usuarios activos con rol {rol}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        alertas = Alerta.objects.bulk_create([
            Alerta(**data, destinatario=u) for u in usuarios
        ])
        return Response(
            AlertaListSerializer(alertas, many=True).data,
            status=status.HTTP_201_CREATED,
        )