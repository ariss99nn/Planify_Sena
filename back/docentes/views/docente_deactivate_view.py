from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from docentes.serializers import DocenteDeactivateSerializer
from users.permissions import IsManager
from docentes.views.base_view_docente import DocenteBaseView


class DocenteDeactivateView(DocenteBaseView):
    """
    PATCH /api/docentes/{id}/deactivate/
    Desactiva el perfil docente. User queda intacto.
    Solo COORDINADOR y ADMINISTRATIVO.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        docente, error = self.get_docente_or_404(pk)
        if error:
            return error

        serializer = DocenteDeactivateSerializer(
            docente,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Perfil docente desactivado correctamente.'})