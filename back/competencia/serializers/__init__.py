from competencia.serializers.asignatura import (
    AsignaturaListSerializer,
    AsignaturaDetailSerializer,
    AsignaturaCreateSerializer,
    AsignaturaUpdateSerializer,
)
from competencia.serializers.competencia import (
    CompetenciaListSerializer,
    CompetenciaDetailSerializer,
    CompetenciaCreateSerializer,
    CompetenciaUpdateSerializer,
)
from competencia.serializers.resultado_aprendizaje import (
    RAPListSerializer,
    RAPDetailSerializer,
    RAPCreateSerializer,
    RAPUpdateSerializer,
)
from competencia.serializers.docente_asignatura import (
    DocenteAsignaturaListSerializer,
    DocenteAsignaturaCreateSerializer,
    DocenteAsignaturaUpdateSerializer,
)

__all__ = [
    'AsignaturaListSerializer', 'AsignaturaDetailSerializer',
    'AsignaturaCreateSerializer', 'AsignaturaUpdateSerializer',
    'CompetenciaListSerializer', 'CompetenciaDetailSerializer',
    'CompetenciaCreateSerializer', 'CompetenciaUpdateSerializer',
    'RAPListSerializer', 'RAPDetailSerializer',
    'RAPCreateSerializer', 'RAPUpdateSerializer',
    'DocenteAsignaturaListSerializer', 'DocenteAsignaturaCreateSerializer',
    'DocenteAsignaturaUpdateSerializer',
]