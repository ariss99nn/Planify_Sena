from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.serializers import (
    DocenteAsignaturaCreateSerializer,
    DocenteAsignaturaListSerializer,
)
from users.permissions import IsManager
from competencia.views.base import CompetenciaBaseView


class DocenteAsignaturaCreateView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = DocenteAsignaturaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asignacion = serializer.save()
        return Response(
            DocenteAsignaturaListSerializer(asignacion).data,
            status=status.HTTP_201_CREATED,
        )