import django_filters
from rest_framework.pagination import PageNumberPagination
from alertas.models.alerta_model import Alerta
from bhorario.models.bloque_horario_model import BloqueHorario


class AlertaPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AlertaFilter(django_filters.FilterSet):
    tipo = django_filters.ChoiceFilter(choices=Alerta.TipoAlerta.choices)
    estado = django_filters.ChoiceFilter(choices=Alerta.EstadoAlerta.choices)
    formato_alerta = django_filters.ChoiceFilter(
        choices=Alerta.FormatoAlerta.choices
    )
    destinatario = django_filters.NumberFilter(field_name='destinatario__id')

    class Meta:
        model = Alerta
        fields = ['tipo', 'estado', 'formato_alerta', 'destinatario']