from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from bhorario.models.bloque_horario_model import BloqueHorario
from bhorario.serializers import BloqueHorarioListSerializer
from users.models.user import User


class HorarioSemanalView(APIView):
    """
    GET /api/horarios/semanal/?docente=<id>&aula=<id>&ficha=<id>
    Devuelve los bloques organizados por día de la semana.
    Todos los roles autenticados pueden ver.
    """
    permission_classes = [IsAuthenticated]

    ORDEN_DIAS = [
        BloqueHorario.DiaSemana.LUNES,
        BloqueHorario.DiaSemana.MARTES,
        BloqueHorario.DiaSemana.MIERCOLES,
        BloqueHorario.DiaSemana.JUEVES,
        BloqueHorario.DiaSemana.VIERNES,
        BloqueHorario.DiaSemana.SABADO,
        BloqueHorario.DiaSemana.DOMINGO,
    ]

    def get_queryset(self, request):
        user = request.user
        qs = BloqueHorario.objects.select_related(
            'aula', 'docente__user', 'ficha__version__programa'
        )

        # Filtros por query params
        docente_id = request.query_params.get('docente')
        aula_id = request.query_params.get('aula')
        ficha_id = request.query_params.get('ficha')
        jornada = request.query_params.get('jornada')

        if docente_id:
            qs = qs.filter(docente_id=docente_id)
        if aula_id:
            qs = qs.filter(aula_id=aula_id)
        if ficha_id:
            qs = qs.filter(ficha_id=ficha_id)
        if jornada:
            qs = qs.filter(jornada=jornada)

        # Restricción por rol
        if user.rol == User.Rol.DOCENTE:
            if not any([docente_id, aula_id, ficha_id]):
                qs = qs.filter(docente__user=user)
        elif user.rol == User.Rol.ESTUDIANTE:
            from ficha.models.ficha_estudiante_model import FichaEstudiante
            ficha_ids = FichaEstudiante.objects.filter(
                estudiante=user, activo=True
            ).values_list('ficha_id', flat=True)
            qs = qs.filter(ficha_id__in=ficha_ids)

        return qs

    def get(self, request):
        qs = self.get_queryset(request)
        bloques = list(qs.order_by('dia_semana', 'hora_inicio'))

        horario = {}
        for dia in self.ORDEN_DIAS:
            dia_display = dict(BloqueHorario.DiaSemana.choices)[dia]
            bloques_dia = [b for b in bloques if b.dia_semana == dia]
            if bloques_dia:
                horario[dia] = {
                    'dia_display': dia_display,
                    'bloques': BloqueHorarioListSerializer(
                        bloques_dia, many=True
                    ).data,
                }

        return Response({
            'total_bloques': len(bloques),
            'dias': horario,
        })