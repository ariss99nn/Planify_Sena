from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from alertas.serializers import AlertaCreateSerializer, AlertaListSerializer
from users.permissions import IsManager
from alertas.views.base import AlertaBaseView


class AlertaCreateView(AlertaBaseView):
    """POST /api/alertas/create/ — solo IsManager crea alertas manuales."""
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = AlertaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        alerta = serializer.save()
        return Response(
            AlertaListSerializer(alerta).data,
            status=status.HTTP_201_CREATED,
        )