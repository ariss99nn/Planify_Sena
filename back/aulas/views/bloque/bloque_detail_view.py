from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import BloqueDetailSerializer
from aulas.views.base_view import AulaBaseView


class BloqueDetailView(AulaBaseView):
    """GET /api/aulas/bloques/{id}/ — todos los roles autenticados."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        bloque, error = self.get_bloque_or_404(pk)
        if error:
            return error
        return Response(BloqueDetailSerializer(bloque).data)