from programa.serializers.programa import (
    ProgramaListSerializer,
    ProgramaDetailSerializer,
    ProgramaCreateSerializer,
    ProgramaUpdateSerializer,
)
from programa.serializers.version import (
    VersionListSerializer,
    VersionDetailSerializer,
    VersionCreateSerializer,
    VersionUpdateSerializer,
)
from programa.serializers.modulo import (
    ModuloListSerializer,
    ModuloDetailSerializer,
    ModuloCreateSerializer,
    ModuloUpdateSerializer,
)
from programa.serializers.docente_modulo import (
    DocenteModuloListSerializer,
    DocenteModuloCreateSerializer,
    DocenteModuloUpdateSerializer,
)

__all__ = [
    'ProgramaListSerializer', 'ProgramaDetailSerializer',
    'ProgramaCreateSerializer', 'ProgramaUpdateSerializer',
    'VersionListSerializer', 'VersionDetailSerializer',
    'VersionCreateSerializer', 'VersionUpdateSerializer',
    'ModuloListSerializer', 'ModuloDetailSerializer',
    'ModuloCreateSerializer', 'ModuloUpdateSerializer',
    'DocenteModuloListSerializer', 'DocenteModuloCreateSerializer',
    'DocenteModuloUpdateSerializer',
]