from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.serializers import (
    DocenteModuloUpdateSerializer,
    DocenteModuloListSerializer,
)
from users.permissions import IsManager
from programa.views.base import ProgramaBaseView


class DocenteModuloUpdateView(ProgramaBaseView):
    """PATCH /api/docentes-modulo/{id}/update/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        asignacion, error = self.get_docente_modulo_or_404(pk)
        if error:
            return error
        serializer = DocenteModuloUpdateSerializer(
            asignacion, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(DocenteModuloListSerializer(asignacion).data)