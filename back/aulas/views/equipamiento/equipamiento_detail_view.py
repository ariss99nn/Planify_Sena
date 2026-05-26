from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import EquipamientoDetailSerializer
from aulas.views.base_view import AulaBaseView


class EquipamientoDetailView(AulaBaseView):
    """GET /api/aulas/equipamiento/{id}/ — todos los roles autenticados."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        equip, error = self.get_equipamiento_or_404(pk)
        if error:
            return error
        return Response(EquipamientoDetailSerializer(equip).data)