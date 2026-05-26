from django.urls import path
from exportacion.views import ExportarView

exportacion_urlpatterns = [
    path('', ExportarView.as_view(), name='exportar'),
]