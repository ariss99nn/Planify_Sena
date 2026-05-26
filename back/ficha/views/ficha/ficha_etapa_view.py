from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ficha.serializers import FichaEtapaUpdateSerializer, FichaDetailSerializer
from users.permissions import IsManager
from ficha.views.base import FichaBaseView


class FichaEtapaView(FichaBaseView):
    """
    PATCH /api/fichas/{id}/etapa/
    Solo IsManager. Registra historial automáticamente via señal.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        ficha, error = self.get_ficha_or_404(pk)
        if error:
            return error
        serializer = FichaEtapaUpdateSerializer(
            ficha,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(FichaDetailSerializer(ficha).data)