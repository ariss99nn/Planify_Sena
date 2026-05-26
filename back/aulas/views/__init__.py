from aulas.views.bloque import (
    BloqueListView, BloqueDetailView,
    BloqueCreateView, BloqueUpdateView,
)
from aulas.views.equipamiento import (
    EquipamientoListView, EquipamientoDetailView,
    EquipamientoCreateView, EquipamientoUpdateView,
)
from aulas.views.aula import (
    AulaListView, AulaDetailView,
    AulaCreateView, AulaUpdateView, AulaEstadoView,
)

__all__ = [
    'BloqueListView', 'BloqueDetailView', 'BloqueCreateView', 'BloqueUpdateView',
    'EquipamientoListView', 'EquipamientoDetailView',
    'EquipamientoCreateView', 'EquipamientoUpdateView',
    'AulaListView', 'AulaDetailView', 'AulaCreateView',
    'AulaUpdateView', 'AulaEstadoView',
]