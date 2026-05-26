from competencia.views.asignatura import (
    AsignaturaListView, AsignaturaDetailView,
    AsignaturaCreateView, AsignaturaUpdateView,
)
from competencia.views.competencia import (
    CompetenciaListView, CompetenciaDetailView,
    CompetenciaCreateView, CompetenciaUpdateView,
)
from competencia.views.resultado_aprendizaje import (
    RAPListView, RAPDetailView,
    RAPCreateView, RAPUpdateView,
)
from competencia.views.docente_asignatura import (
    DocenteAsignaturaListView,
    DocenteAsignaturaCreateView,
    DocenteAsignaturaUpdateView,
)

__all__ = [
    'AsignaturaListView', 'AsignaturaDetailView',
    'AsignaturaCreateView', 'AsignaturaUpdateView',
    'CompetenciaListView', 'CompetenciaDetailView',
    'CompetenciaCreateView', 'CompetenciaUpdateView',
    'RAPListView', 'RAPDetailView',
    'RAPCreateView', 'RAPUpdateView',
    'DocenteAsignaturaListView', 'DocenteAsignaturaCreateView',
    'DocenteAsignaturaUpdateView',
]