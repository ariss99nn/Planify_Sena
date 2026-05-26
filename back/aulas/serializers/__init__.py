from aulas.serializers.bloque import (
    BloqueListSerializer,
    BloqueDetailSerializer,
    BloqueCreateSerializer,
    BloqueUpdateSerializer,
)
from aulas.serializers.equipamiento import (
    EquipamientoListSerializer,
    EquipamientoDetailSerializer,
    EquipamientoCreateSerializer,
    EquipamientoUpdateSerializer,
)
from aulas.serializers.aula import (
    AulaListSerializer,
    AulaDetailSerializer,
    AulaCreateSerializer,
    AulaUpdateSerializer,
    AulaEstadoSerializer,
)

__all__ = [
    'BloqueListSerializer', 'BloqueDetailSerializer',
    'BloqueCreateSerializer', 'BloqueUpdateSerializer',
    'EquipamientoListSerializer', 'EquipamientoDetailSerializer',
    'EquipamientoCreateSerializer', 'EquipamientoUpdateSerializer',
    'AulaListSerializer', 'AulaDetailSerializer',
    'AulaCreateSerializer', 'AulaUpdateSerializer', 'AulaEstadoSerializer',
]