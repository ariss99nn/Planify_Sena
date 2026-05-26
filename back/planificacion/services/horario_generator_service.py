import logging
from datetime import time
from django.db import transaction
from bhorario.services.bloque_service import BloqueHorarioService, ColisionError
from bhorario.models.bloque_horario_model import BloqueHorario

logger = logging.getLogger(__name__)

SLOTS_POR_JORNADA = {
    BloqueHorario.Jornada.MANANA: [
        (time(6, 0), time(8, 0)),
        (time(8, 0), time(10, 0)),
        (time(10, 0), time(12, 0)),
    ],
    BloqueHorario.Jornada.TARDE: [
        (time(12, 0), time(14, 0)),
        (time(14, 0), time(16, 0)),
        (time(16, 0), time(18, 0)),
    ],
    BloqueHorario.Jornada.NOCHE: [
        (time(18, 0), time(20, 0)),
        (time(20, 0), time(22, 0)),
    ],
}

DIAS_HABILES = [
    BloqueHorario.DiaSemana.LUNES,
    BloqueHorario.DiaSemana.MARTES,
    BloqueHorario.DiaSemana.MIERCOLES,
    BloqueHorario.DiaSemana.JUEVES,
    BloqueHorario.DiaSemana.VIERNES,
]


class HorarioGeneratorService:
    """
    Genera bloques horarios automáticamente desde un PlanTrimestral aprobado.

    Algoritmo:
    1. Ordena items: PRINCIPAL primero, TRANSVERSAL al final.
    2. Para cada item busca slots donde docente, aula y ficha estén libres.
    3. Crea el bloque y lo vincula al item.
    4. Si no encuentra slot, registra el conflicto sin abortar.
    """

    def __init__(self, plan, dias=None):
        from planificacion.models.plan_trimestral_model import PlanTrimestral
        if not plan.aprobado:
            raise ValueError('El plan debe estar aprobado antes de generar horarios.')
        self.plan = plan
        self.jornada = plan.ficha.jornada
        self.dias = dias or DIAS_HABILES
        self.slots = SLOTS_POR_JORNADA.get(self.jornada, [])
        self.bloques_creados = []
        self.conflictos = []

    @transaction.atomic
    def generar(self) -> dict:
        from planificacion.models.bloque_competencia_model import BloqueCompetencia

        items = self.plan.items.select_related(
            'competencia', 'docente'
        ).order_by('competencia__tipo', 'orden')

        for item in items:
            horas_restantes = item.horas_asignadas
            for dia in self.dias:
                if horas_restantes <= 0:
                    break
                for h_inicio, h_fin in self.slots:
                    if horas_restantes <= 0:
                        break

                    from bhorario.services.bloque_service import BloqueHorarioService
                    disponibilidad = BloqueHorarioService.verificar_disponibilidad(
                        dia=dia,
                        hora_inicio=h_inicio,
                        hora_fin=h_fin,
                        docente=item.docente,
                        ficha=self.plan.ficha,
                    )
                    if not disponibilidad['disponible']:
                        continue

                    try:
                        bloque = BloqueHorarioService.crear_bloque({
                            'dia_semana': dia,
                            'hora_inicio': h_inicio,
                            'hora_fin': h_fin,
                            'jornada': self.jornada,
                            'docente': item.docente,
                            'ficha': self.plan.ficha,
                        })
                        BloqueCompetencia.objects.create(
                            bloque=bloque,
                            item_plan=item,
                            horas_ejecutadas=2,
                        )
                        self.bloques_creados.append(bloque.pk)
                        horas_restantes -= 2
                    except ColisionError as e:
                        self.conflictos.append({
                            'item': str(item),
                            'dia': dia,
                            'hora': f'{h_inicio}-{h_fin}',
                            'error': str(e),
                        })

        return {
            'bloques_creados': len(self.bloques_creados),
            'conflictos': self.conflictos,
            'completado': len(self.conflictos) == 0,
        }