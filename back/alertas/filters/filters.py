import django_filters
from rest_framework.pagination import PageNumberPagination
from alertas.models.alerta_model import Alerta


class AlertaPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AlertaFilter(django_filters.FilterSet):
    tipo           = django_filters.ChoiceFilter(choices=Alerta.TipoAlerta.choices)
    estado         = django_filters.ChoiceFilter(choices=Alerta.EstadoAlerta.choices)
    formato_alerta = django_filters.ChoiceFilter(choices=Alerta.FormatoAlerta.choices)
    # NumberFilter sigue siendo correcto para IDs; no es necesario ModelChoiceFilter
    # en APIs donde el cliente envía el ID numérico directamente.
    destinatario   = django_filters.NumberFilter(field_name='destinatario__id')
    leidas         = django_filters.BooleanFilter(
        method='filter_leidas',
        label='Solo no leídas',
    )

    def filter_leidas(self, queryset, name, value):
        if value:
            return queryset.exclude(estado=Alerta.EstadoAlerta.LEIDA)
        return queryset

    class Meta:
        model  = Alerta
        fields = ['tipo', 'estado', 'formato_alerta', 'destinatario']