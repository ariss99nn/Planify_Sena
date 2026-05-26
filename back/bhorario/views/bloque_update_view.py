from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bhorario.serializers import BloqueHorarioUpdateSerializer, BloqueHorarioDetailSerializer
from users.permissions import IsManager
from bhorario.views.base import BhorarioBaseView


class BloqueHorarioUpdateView(BhorarioBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        bloque, error = self.get_bloque_or_404(pk)
        if error:
            return error
        serializer = BloqueHorarioUpdateSerializer(
            bloque, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(BloqueHorarioDetailSerializer(bloque).data)