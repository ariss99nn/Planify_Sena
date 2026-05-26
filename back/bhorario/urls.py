from django.urls import path
from bhorario.views import (
    BloqueHorarioListView,
    BloqueHorarioDetailView,
    BloqueHorarioCreateView,
    BloqueHorarioUpdateView,
)
from bhorario.views.disponibilidad_view import DisponibilidadView
from bhorario.views.horario_semanal_view import HorarioSemanalView

bhorario_urlpatterns = [
    path('',                    BloqueHorarioListView.as_view(),   name='bhorario-list'),
    path('create/',             BloqueHorarioCreateView.as_view(), name='bhorario-create'),
    path('disponibilidad/',     DisponibilidadView.as_view(),      name='bhorario-disponibilidad'),
    path('<int:pk>/',           BloqueHorarioDetailView.as_view(), name='bhorario-detail'),
    path('<int:pk>/update/',    BloqueHorarioUpdateView.as_view(), name='bhorario-update'),
    path('semanal/', HorarioSemanalView.as_view(), name='bhorario-semanal'),
]