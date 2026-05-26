from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from competencia.serializers import RAPDetailSerializer
from competencia.views.base import CompetenciaBaseView
from users.models.user import User


class RAPDetailView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        rap, error = self.get_rap_or_404(pk)
        if error:
            return error

        user = request.user
        if user.rol == User.Rol.DOCENTE:
            from competencia.models.docente_asignatura_model import DocenteAsignatura
            if not DocenteAsignatura.objects.filter(
                docente=user,
                asignatura=rap.competencia.asignatura,
                activo=True,
            ).exists():
                return Response(
                    {'detail': 'No tienes acceso a este resultado.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_model import Ficha
            if not Ficha.objects.filter(
                estado=True,
                version__modulos=rap.competencia.asignatura.modulo,
            ).exists():
                return Response(
                    {'detail': 'No tienes acceso a este resultado.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(RAPDetailSerializer(rap).data)