from planificacion.views.plan_trimestral_view import (
    PlanTrimestralListView,
    PlanTrimestralDetailView,
    PlanTrimestralCreateView,
    PlanTrimestralUpdateView,
    PlanTrimestralAprobarView,
    GenerarHorarioView,
)
from planificacion.views.item_plan_view import (
    ItemPlanListView,
    ItemPlanCreateView,
    ItemPlanUpdateView,
)
from planificacion.views.bloque_competencia_views import (
    BloqueCompetenciaListView,
    BloqueCompetenciaCreateView,
)

__all__ = [
    'PlanTrimestralListView', 'PlanTrimestralDetailView',
    'PlanTrimestralCreateView', 'PlanTrimestralUpdateView',
    'PlanTrimestralAprobarView', 'GenerarHorarioView',
    'ItemPlanListView', 'ItemPlanCreateView', 'ItemPlanUpdateView',
    'BloqueCompetenciaListView', 'BloqueCompetenciaCreateView',
]