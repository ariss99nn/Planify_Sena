from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import EquipamientoUpdateSerializer, EquipamientoDetailSerializer
from users.permissions import IsManager
from aulas.views.base_view import AulaBaseView


class EquipamientoUpdateView(AulaBaseView):
    """PATCH /api/aulas/equipamiento/{id}/update/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        equip, error = self.get_equipamiento_or_404(pk)
        if error:
            return error
        serializer = EquipamientoUpdateSerializer(equip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # CORRECCIÓN: usar serializer.instance (objeto post-save)
        # en lugar de 'equip' (stale, pre-save).
        return Response(EquipamientoDetailSerializer(serializer.instance).data)