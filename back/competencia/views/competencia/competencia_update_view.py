from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.serializers import CompetenciaUpdateSerializer, CompetenciaDetailSerializer
from users.permissions import IsManager
from competencia.views.base import CompetenciaBaseView


class CompetenciaUpdateView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        competencia, error = self.get_competencia_or_404(pk)
        if error:
            return error
        serializer = CompetenciaUpdateSerializer(
            competencia, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CompetenciaDetailSerializer(competencia).data)