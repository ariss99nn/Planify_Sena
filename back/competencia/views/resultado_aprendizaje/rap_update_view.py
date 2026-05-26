from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.serializers import RAPUpdateSerializer, RAPDetailSerializer
from users.permissions import IsManager
from competencia.views.base import CompetenciaBaseView


class RAPUpdateView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        rap, error = self.get_rap_or_404(pk)
        if error:
            return error
        serializer = RAPUpdateSerializer(rap, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(RAPDetailSerializer(rap).data)