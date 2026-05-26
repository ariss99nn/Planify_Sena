from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ficha.models.ficha_model import Ficha
from ficha.models.ficha_estudiante_model import FichaEstudiante
from ficha.models.reasignacion_ficha_model import ReasignacionFicha
from ficha.models.historial_etapa_model import HistorialEtapa


class FichaBaseView(APIView):

    def get_ficha_or_404(self, pk):
        obj = Ficha.objects.select_related(
            'version__programa',
            'jefe_grupo',
        ).filter(pk=pk).first()
        if obj is None:
            return None, Response(
                {'detail': 'Ficha no encontrada.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return obj, None

    def get_ficha_estudiante_or_404(self, ficha, estudiante_pk):
        obj = FichaEstudiante.objects.select_related(
            'estudiante', 'ficha'
        ).filter(ficha=ficha, pk=estudiante_pk).first()
        if obj is None:
            return None, Response(
                {'detail': 'Estudiante no encontrado en esta ficha.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return obj, None

    def es_jefe_de_ficha(self, user, ficha):
        return ficha.jefe_grupo_id == user.pk