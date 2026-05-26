from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from competencia.serializers import CompetenciaDetailSerializer
from competencia.views.base import CompetenciaBaseView
from users.models.user import User


class CompetenciaDetailView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        competencia, error = self.get_competencia_or_404(pk)
        if error:
            return error

        user = request.user
        if user.rol == User.Rol.DOCENTE:
            from competencia.models.docente_asignatura_model import DocenteAsignatura
            if not DocenteAsignatura.objects.filter(
                docente=user,
                asignatura=competencia.asignatura,
                activo=True,
            ).exists():
                return Response(
                    {'detail': 'No tienes acceso a esta competencia.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_model import Ficha
            if not Ficha.objects.filter(
                estado=True,
                version__modulos=competencia.asignatura.modulo,
            ).exists():
                return Response(
                    {'detail': 'No tienes acceso a esta competencia.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(CompetenciaDetailSerializer(competencia).data)