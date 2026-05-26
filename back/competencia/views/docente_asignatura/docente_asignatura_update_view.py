from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.serializers import (
    DocenteAsignaturaUpdateSerializer,
    DocenteAsignaturaListSerializer,
)
from users.permissions import IsManager
from competencia.views.base import CompetenciaBaseView


class DocenteAsignaturaUpdateView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        asignacion, error = self.get_docente_asignatura_or_404(pk)
        if error:
            return error
        serializer = DocenteAsignaturaUpdateSerializer(
            asignacion, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(DocenteAsignaturaListSerializer(asignacion).data)