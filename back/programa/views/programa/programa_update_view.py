from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.serializers import ProgramaUpdateSerializer, ProgramaDetailSerializer
from users.permissions import IsManager
from programa.views.base import ProgramaBaseView


class ProgramaUpdateView(ProgramaBaseView):
    """PATCH /api/programas/{id}/update/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        programa, error = self.get_programa_or_404(pk)
        if error:
            return error
        serializer = ProgramaUpdateSerializer(
            programa, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProgramaDetailSerializer(programa).data)