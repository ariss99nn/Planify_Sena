from programa.views.programa import (
    ProgramaListView, ProgramaDetailView,
    ProgramaCreateView, ProgramaUpdateView,
)
from programa.views.version import (
    VersionListView, VersionDetailView,
    VersionCreateView, VersionUpdateView,
)
from programa.views.modulo import (
    ModuloListView, ModuloDetailView,
    ModuloCreateView, ModuloUpdateView,
)
from programa.views.docente_modulo import (
    DocenteModuloListView,
    DocenteModuloCreateView,
    DocenteModuloUpdateView,
)

__all__ = [
    'ProgramaListView', 'ProgramaDetailView',
    'ProgramaCreateView', 'ProgramaUpdateView',
    'VersionListView', 'VersionDetailView',
    'VersionCreateView', 'VersionUpdateView',
    'ModuloListView', 'ModuloDetailView',
    'ModuloCreateView', 'ModuloUpdateView',
    'DocenteModuloListView', 'DocenteModuloCreateView',
    'DocenteModuloUpdateView',
]