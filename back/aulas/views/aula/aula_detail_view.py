from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from aulas.serializers import AulaDetailSerializer
from aulas.views.base_view import AulaBaseView


class AulaDetailView(AulaBaseView):
    """GET /api/aulas/{id}/ — todos los roles autenticados."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        aula, error = self.get_aula_or_404(pk)
        if error:
            return error
        return Response(AulaDetailSerializer(aula).data)