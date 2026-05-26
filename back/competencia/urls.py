from django.urls import path
from competencia.views import (
    AsignaturaListView, AsignaturaDetailView,
    AsignaturaCreateView, AsignaturaUpdateView,
    CompetenciaListView, CompetenciaDetailView,
    CompetenciaCreateView, CompetenciaUpdateView,
    RAPListView, RAPDetailView,
    RAPCreateView, RAPUpdateView,
    DocenteAsignaturaListView,
    DocenteAsignaturaCreateView,
    DocenteAsignaturaUpdateView,
)

asignatura_urlpatterns = [
    path('',                 AsignaturaListView.as_view(),   name='asignatura-list'),
    path('create/',          AsignaturaCreateView.as_view(), name='asignatura-create'),
    path('<int:pk>/',        AsignaturaDetailView.as_view(), name='asignatura-detail'),
    path('<int:pk>/update/', AsignaturaUpdateView.as_view(), name='asignatura-update'),
]

competencia_urlpatterns = [
    path('',                 CompetenciaListView.as_view(),   name='competencia-list'),
    path('create/',          CompetenciaCreateView.as_view(), name='competencia-create'),
    path('<int:pk>/',        CompetenciaDetailView.as_view(), name='competencia-detail'),
    path('<int:pk>/update/', CompetenciaUpdateView.as_view(), name='competencia-update'),
]

rap_urlpatterns = [
    path('',                 RAPListView.as_view(),   name='rap-list'),
    path('create/',          RAPCreateView.as_view(), name='rap-create'),
    path('<int:pk>/',        RAPDetailView.as_view(), name='rap-detail'),
    path('<int:pk>/update/', RAPUpdateView.as_view(), name='rap-update'),
]

docente_asignatura_urlpatterns = [
    path('',                 DocenteAsignaturaListView.as_view(),   name='docente-asignatura-list'),
    path('create/',          DocenteAsignaturaCreateView.as_view(), name='docente-asignatura-create'),
    path('<int:pk>/update/', DocenteAsignaturaUpdateView.as_view(), name='docente-asignatura-update'),
]