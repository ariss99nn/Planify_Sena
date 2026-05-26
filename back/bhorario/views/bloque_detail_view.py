from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from bhorario.serializers import BloqueHorarioDetailSerializer
from bhorario.views.base import BhorarioBaseView
from users.models.user import User


class BloqueHorarioDetailView(BhorarioBaseView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        bloque, error = self.get_bloque_or_404(pk)
        if error:
            return error

        user = request.user
        if user.rol == User.Rol.DOCENTE:
            if not (bloque.docente and bloque.docente.user == user):
                return Response(
                    {'detail': 'No tienes acceso a este bloque.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_estudiante_model import FichaEstudiante
            if not FichaEstudiante.objects.filter(
                estudiante=user,
                ficha=bloque.ficha,
                activo=True,
            ).exists():
                return Response(
                    {'detail': 'No tienes acceso a este bloque.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(BloqueHorarioDetailSerializer(bloque).data)