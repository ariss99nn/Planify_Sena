from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.serializers import AsignaturaUpdateSerializer, AsignaturaDetailSerializer
from users.permissions import IsManager
from competencia.views.base import CompetenciaBaseView


class AsignaturaUpdateView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        asignatura, error = self.get_asignatura_or_404(pk)
        if error:
            return error
        serializer = AsignaturaUpdateSerializer(
            asignatura, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AsignaturaDetailSerializer(asignatura).data)