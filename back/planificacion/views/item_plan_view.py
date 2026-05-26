from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from planificacion.serializers import (
    ItemPlanListSerializer,
    ItemPlanCreateSerializer,
    ItemPlanUpdateSerializer,
)
from planificacion.filters import ItemPlanFilter, PlanificacionPagination
from planificacion.models.item_plan_model import ItemPlan
from planificacion.views.base import PlanificacionBaseView
from users.permissions import IsManager


class ItemPlanListView(PlanificacionBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        queryset = ItemPlan.objects.select_related(
            'competencia', 'docente__user', 'plan__ficha'
        )
        filterset = ItemPlanFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = PlanificacionPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            ItemPlanListSerializer(page, many=True).data
        )


class ItemPlanCreateView(PlanificacionBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = ItemPlanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(
            ItemPlanListSerializer(item).data,
            status=status.HTTP_201_CREATED,
        )


class ItemPlanUpdateView(PlanificacionBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        item, error = self.get_item_or_404(pk)
        if error:
            return error
        serializer = ItemPlanUpdateSerializer(
            item, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ItemPlanListSerializer(item).data)