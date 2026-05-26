import logging
from django.db import transaction
from planificacion.models.plan_trimestral_model import PlanTrimestral
from planificacion.models.item_plan_model import ItemPlan

logger = logging.getLogger(__name__)


class PlanService:

    @staticmethod
    @transaction.atomic
    def aprobar_plan(plan: PlanTrimestral, usuario) -> PlanTrimestral:
        if not plan.items.exists():
            raise ValueError('No se puede aprobar un plan sin items.')
        if plan.aprobado:
            raise ValueError('El plan ya está aprobado.')
        from django.utils import timezone
        plan.aprobado = True
        plan.aprobado_por = usuario
        plan.fecha_aprobacion = timezone.now()
        plan.save(update_fields=['aprobado', 'aprobado_por', 'fecha_aprobacion'])
        logger.info("Plan %s aprobado por %s", plan, usuario.email)
        return plan

    @staticmethod
    def calcular_carga_docente(docente, trimestre: int) -> dict:
        """Calcula las horas asignadas a un docente en un trimestre."""
        items = ItemPlan.objects.filter(
            docente=docente,
            plan__trimestre=trimestre,
            plan__aprobado=True,
        ).select_related('competencia', 'plan__ficha')

        total_horas = sum(i.horas_asignadas for i in items)
        max_horas = docente.horas_max_semanales * 12  # 12 semanas por trimestre

        return {
            'docente': docente.user.nombre,
            'trimestre': trimestre,
            'horas_planificadas': total_horas,
            'horas_maximas': max_horas,
            'porcentaje_carga': round((total_horas / max_horas) * 100, 1) if max_horas else 0,
            'sobrecargado': total_horas > max_horas,
            'items': [
                {
                    'ficha': i.plan.ficha.codigo_ficha,
                    'competencia': i.competencia.codigo,
                    'horas': i.horas_asignadas,
                }
                for i in items
            ],
        }