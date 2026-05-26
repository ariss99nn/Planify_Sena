from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from programa.serializers import ProgramaDetailSerializer
from programa.views.base import ProgramaBaseView
from users.models.user import User


class ProgramaDetailView(ProgramaBaseView):
    """
    GET /api/programas/{id}/
    ESTUDIANTE: solo puede ver el programa de su ficha activa.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        programa, error = self.get_programa_or_404(pk)
        if error:
            return error

        user = request.user
        if user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_model import Ficha
            tiene_ficha = Ficha.objects.filter(
                estado=True,
                version__programa=programa,
            ).exists()
            if not tiene_ficha:
                return Response(
                    {'detail': 'No tienes acceso a este programa.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return Response(ProgramaDetailSerializer(programa).data)