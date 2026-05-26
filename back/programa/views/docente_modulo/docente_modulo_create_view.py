from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from programa.serializers import (
    DocenteModuloCreateSerializer,
    DocenteModuloListSerializer,
)
from users.permissions import IsManager
from programa.views.base import ProgramaBaseView


class DocenteModuloCreateView(ProgramaBaseView):
    """POST /api/docentes-modulo/create/ — solo IsManager."""
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = DocenteModuloCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asignacion = serializer.save()
        return Response(
            DocenteModuloListSerializer(asignacion).data,
            status=status.HTTP_201_CREATED,
        )