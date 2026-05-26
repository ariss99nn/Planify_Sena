from django.urls import path
from reportes.views.reporte_solicitar_view import (
    SolicitarReporteView,
    EstadoReporteView,
)

reportes_urlpatterns = [
    path('solicitar/',   SolicitarReporteView.as_view(), name='reporte-solicitar'),
    path('<int:pk>/',    EstadoReporteView.as_view(),    name='reporte-estado'),
]