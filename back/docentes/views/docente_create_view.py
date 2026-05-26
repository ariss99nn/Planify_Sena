from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from docentes.serializers import DocenteCreateSerializer, DocenteDetailSerializer
from users.permissions import IsManager
from docentes.views.base_view_docente import DocenteBaseView


class DocenteCreateView(DocenteBaseView):
    """
    POST /api/docentes/
    Solo COORDINADOR y ADMINISTRATIVO.
    El user_id debe corresponder a un User con rol=DOCENTE y estado=True.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = DocenteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        docente = serializer.save()
        return Response(
            DocenteDetailSerializer(docente).data,
            status=status.HTTP_201_CREATED,
        )