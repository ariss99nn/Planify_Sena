from django.urls import path
from docentes.views import (
    DocenteListView,
    DocenteDetailView,
    DocenteCreateView,
    DocenteUpdateView,
    DocenteDeactivateView,
)

docente_urlpatterns = [
    path('',                        DocenteListView.as_view(),       name='docente-list'),
    path('create/',                 DocenteCreateView.as_view(),     name='docente-create'),
    path('<int:pk>/',               DocenteDetailView.as_view(),     name='docente-detail'),
    path('<int:pk>/update/',        DocenteUpdateView.as_view(),     name='docente-update'),
    path('<int:pk>/deactivate/',    DocenteDeactivateView.as_view(), name='docente-deactivate'),
]