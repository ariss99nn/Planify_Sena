from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bhorario.models.bloque_horario_model import BloqueHorario


class BhorarioBaseView(APIView):

    def get_bloque_or_404(self, pk):
        obj = BloqueHorario.objects.select_related(
            'aula', 'docente__user', 'ficha__version__programa'
        ).filter(pk=pk).first()
        if obj is None:
            return None, Response(
                {'detail': 'Bloque de horario no encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return obj, None