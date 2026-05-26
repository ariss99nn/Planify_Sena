from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ficha.serializers import (
    FichaEstudianteUpdateSerializer,
    FichaEstudianteListSerializer,
)
from users.permissions import IsManager
from ficha.views.base import FichaBaseView


class FichaEstudianteUpdateView(FichaBaseView):
    """PATCH /api/fichas/{id}/estudiantes/{eid}/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk, eid):
        ficha, error = self.get_ficha_or_404(pk)
        if error:
            return error

        relacion, error = self.get_ficha_estudiante_or_404(ficha, eid)
        if error:
            return error

        serializer = FichaEstudianteUpdateSerializer(
            relacion, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(FichaEstudianteListSerializer(relacion).data)