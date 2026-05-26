from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from planificacion.models.plan_trimestral_model import PlanTrimestral
from planificacion.serializers import (
    PlanTrimestralListSerializer,
    PlanTrimestralDetailSerializer,
    PlanTrimestralCreateSerializer,
    PlanTrimestralUpdateSerializer,
    PlanTrimestralAprobarSerializer,
)
from planificacion.filters import PlanTrimestralFilter, PlanificacionPagination
from planificacion.services.horario_generator_service import HorarioGeneratorService
from planificacion.views.base import PlanificacionBaseView
from users.permissions import IsManager
from users.models.user import User


class PlanTrimestralListView(PlanificacionBaseView):
    """
    GET /api/planes/
    IsManager: todos los planes.
    DOCENTE: planes donde es jefe de grupo o tiene items asignados.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        qs = PlanTrimestral.objects.select_related(
            'ficha__version__programa', 'aprobado_por'
        )
        if user.rol in {User.Rol.COORDINADOR, User.Rol.ADMIN}:
            return qs
        if user.rol == User.Rol.DOCENTE:
            from docentes.models.docente import Docente
            try:
                docente = Docente.objects.get(user=user)
                jefe_ids = qs.filter(
                    ficha__jefe_grupo=user
                ).values_list('id', flat=True)
                item_ids = qs.filter(
                    items__docente=docente
                ).values_list('id', flat=True)
                return qs.filter(
                    id__in=set(list(jefe_ids) + list(item_ids))
                ).distinct()
            except Docente.DoesNotExist:
                return qs.none()
        return qs.none()

    def get(self, request):
        queryset = self.get_queryset(request)
        filterset = PlanTrimestralFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        paginator = PlanificacionPagination()
        page = paginator.paginate_queryset(filterset.qs, request)
        return paginator.get_paginated_response(
            PlanTrimestralListSerializer(page, many=True).data
        )


class PlanTrimestralDetailView(PlanificacionBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, pk):
        plan, error = self.get_plan_or_404(pk)
        if error:
            return error
        return Response(PlanTrimestralDetailSerializer(plan).data)


class PlanTrimestralCreateView(PlanificacionBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = PlanTrimestralCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.save()
        return Response(
            PlanTrimestralDetailSerializer(plan).data,
            status=status.HTTP_201_CREATED,
        )


class PlanTrimestralUpdateView(PlanificacionBaseView):
    permission_classes = [IsAuthenticated, IsManager]

    def patch(self, request, pk):
        plan, error = self.get_plan_or_404(pk)
        if error:
            return error
        if plan.aprobado:
            return Response(
                {'detail': 'No se puede editar un plan aprobado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PlanTrimestralUpdateSerializer(
            plan, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PlanTrimestralDetailSerializer(plan).data)


class PlanTrimestralAprobarView(PlanificacionBaseView):
    """PATCH /api/planes/{id}/aprobar/ — solo COORDINADOR."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.rol != User.Rol.COORDINADOR:
            return Response(
                {'detail': 'Solo el coordinador puede aprobar planes.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        plan, error = self.get_plan_or_404(pk)
        if error:
            return error
        serializer = PlanTrimestralAprobarSerializer(
            plan,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PlanTrimestralDetailSerializer(plan).data)


class GenerarHorarioView(PlanificacionBaseView):
    """
    POST /api/planes/{id}/generar-horario/
    Genera bloques horarios automáticamente desde el plan aprobado.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, pk):
        plan, error = self.get_plan_or_404(pk)
        if error:
            return error
        if not plan.aprobado:
            return Response(
                {'detail': 'El plan debe estar aprobado para generar horarios.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            generador = HorarioGeneratorService(plan)
            resultado = generador.generar()
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(resultado, status=status.HTTP_201_CREATED)