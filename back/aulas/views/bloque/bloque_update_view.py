from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import BloqueUpdateSerializer, BloqueDetailSerializer
from users.permissions import IsManager
from aulas.views.base_view import AulaBaseView


class BloqueUpdateView(AulaBaseView):
    """PATCH /api/aulas/bloques/{id}/update/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        bloque, error = self.get_bloque_or_404(pk)
        if error:
            return error
        serializer = BloqueUpdateSerializer(bloque, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # CORRECCIÓN: usar serializer.instance (objeto post-save)
        # en lugar de 'bloque' (stale, pre-save).
        return Response(BloqueDetailSerializer(serializer.instance).data)