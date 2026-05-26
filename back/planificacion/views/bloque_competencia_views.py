from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from planificacion.serializers import (
    BloqueCompetenciaListSerializer,
    BloqueCompetenciaCreateSerializer,
)
from planificacion.models.bloque_competencia_model import BloqueCompetencia
from planificacion.views.base import PlanificacionBaseView
from users.permissions import IsManager


class BloqueCompetenciaListView(PlanificacionBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        plan_id = request.query_params.get('plan')
        item_id = request.query_params.get('item')
        qs = BloqueCompetencia.objects.select_related(
            'bloque__docente__user',
            'bloque__aula',
            'item_plan__competencia',
        )
        if plan_id:
            qs = qs.filter(item_plan__plan_id=plan_id)
        if item_id:
            qs = qs.filter(item_plan_id=item_id)
        return Response(BloqueCompetenciaListSerializer(qs, many=True).data)


class BloqueCompetenciaCreateView(PlanificacionBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = BloqueCompetenciaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bc = serializer.save()
        return Response(
            BloqueCompetenciaListSerializer(bc).data,
            status=status.HTTP_201_CREATED,
        )