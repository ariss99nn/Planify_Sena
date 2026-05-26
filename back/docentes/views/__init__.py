from docentes.views.base_view_docente import DocenteBaseView
from docentes.views.docente_list_view import DocenteListView
from docentes.views.docente_detail_view import DocenteDetailView
from docentes.views.docente_create_view import DocenteCreateView
from docentes.views.docente_update_view import DocenteUpdateView
from docentes.views.docente_deactivate_view import DocenteDeactivateView

__all__ = [
    'DocenteBaseView',
    'DocenteListView',
    'DocenteDetailView',
    'DocenteCreateView',
    'DocenteUpdateView',
    'DocenteDeactivateView',
]