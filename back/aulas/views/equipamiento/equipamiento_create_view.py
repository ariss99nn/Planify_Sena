from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import EquipamientoCreateSerializer, EquipamientoDetailSerializer
from users.permissions import IsManager
from aulas.views.base_view import AulaBaseView


class EquipamientoCreateView(AulaBaseView):
    """POST /api/aulas/equipamiento/create/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = EquipamientoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        equip = serializer.save()
        return Response(
            EquipamientoDetailSerializer(equip).data,
            status=status.HTTP_201_CREATED,
        )