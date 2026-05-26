from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from competencia.serializers import AsignaturaDetailSerializer
from competencia.views.base import CompetenciaBaseView
from users.models.user import User


class AsignaturaDetailView(CompetenciaBaseView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        asignatura, error = self.get_asignatura_or_404(pk)
        if error:
            return error

        user = request.user

        if user.rol == User.Rol.DOCENTE:
            from competencia.models.docente_asignatura_model import DocenteAsignatura
            tiene_asignacion = DocenteAsignatura.objects.filter(
                docente=user, asignatura=asignatura, activo=True
            ).exists()
            if not tiene_asignacion:
                return Response(
                    {'detail': 'No tienes acceso a esta asignatura.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_model import Ficha
            tiene_ficha = Ficha.objects.filter(
                estado=True,
                version__modulos=asignatura.modulo,
            ).exists()
            if not tiene_ficha:
                return Response(
                    {'detail': 'No tienes acceso a esta asignatura.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(AsignaturaDetailSerializer(asignatura).data)