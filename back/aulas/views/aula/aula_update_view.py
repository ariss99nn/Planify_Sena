from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import AulaUpdateSerializer, AulaDetailSerializer
from users.permissions import IsManager
from aulas.views.base_view import AulaBaseView


class AulaUpdateView(AulaBaseView):
    """PATCH /api/aulas/{id}/update/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        aula, error = self.get_aula_or_404(pk)
        if error:
            return error
        serializer = AulaUpdateSerializer(aula, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # CORRECCIÓN: usar serializer.instance (objeto post-save)
        # en lugar de 'aula' (stale, pre-save).
        return Response(AulaDetailSerializer(serializer.instance).data)