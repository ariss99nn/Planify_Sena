from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from bhorario.services.bloque_service import BloqueHorarioService
from bhorario.models.bloque_horario_model import BloqueHorario
from docentes.models.docente import Docente
from aulas.models.aula import Aula
from ficha.models.ficha_model import Ficha


class DisponibilidadView(APIView):
    """
    POST /api/horarios/disponibilidad/
    Verifica si docente, aula y ficha están disponibles en un intervalo.
    No crea nada — solo consulta.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            hora_inicio = data['hora_inicio']
            hora_fin = data['hora_fin']
            dia = data['dia_semana']
        except KeyError as e:
            return Response({'detail': f'Campo requerido: {e}'}, status=400)

        docente = None
        aula = None
        ficha = None

        if data.get('docente'):
            docente = Docente.objects.filter(pk=data['docente']).first()
        if data.get('aula'):
            aula = Aula.objects.filter(pk=data['aula']).first()
        if data.get('ficha'):
            ficha = Ficha.objects.filter(pk=data['ficha']).first()

        resultado = BloqueHorarioService.verificar_disponibilidad(
            dia=dia,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            docente=docente,
            aula=aula,
            ficha=ficha,
            excluir_pk=data.get('excluir_pk'),
        )

        disponible = all([
            resultado['docente_disponible'],
            resultado['aula_disponible'],
            resultado['ficha_disponible'],
        ])

        return Response({
            'disponible': disponible,
            **resultado,
        })