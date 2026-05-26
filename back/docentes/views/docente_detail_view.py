from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from docentes.serializers import DocenteDetailSerializer
from users.permissions import IsManager
from docentes.views.base_view_docente import DocenteBaseView


class DocenteDetailView(DocenteBaseView):
    """
    GET /api/docentes/{id}/
    Solo COORDINADOR y ADMINISTRATIVO.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, pk):
        docente, error = self.get_docente_or_404(pk)
        if error:
            return error
        return Response(DocenteDetailSerializer(docente).data)