from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from competencia.serializers import CompetenciaCreateSerializer, CompetenciaDetailSerializer
from users.permissions import IsManager
from competencia.views.base import CompetenciaBaseView


class CompetenciaCreateView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = CompetenciaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comp = serializer.save()
        return Response(
            CompetenciaDetailSerializer(comp).data,
            status=status.HTTP_201_CREATED,
        )