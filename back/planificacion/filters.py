import django_filters
from rest_framework.pagination import PageNumberPagination
from planificacion.models.plan_trimestral_model import PlanTrimestral
from planificacion.models.item_plan_model import ItemPlan


class PlanificacionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PlanTrimestralFilter(django_filters.FilterSet):
    ficha = django_filters.NumberFilter(field_name='ficha__id')
    trimestre = django_filters.NumberFilter()
    aprobado = django_filters.BooleanFilter()
    programa = django_filters.NumberFilter(
        field_name='ficha__version__programa__id'
    )

    class Meta:
        model = PlanTrimestral
        fields = ['ficha', 'trimestre', 'aprobado']


class ItemPlanFilter(django_filters.FilterSet):
    plan = django_filters.NumberFilter(field_name='plan__id')
    docente = django_filters.NumberFilter(field_name='docente__id')
    completado = django_filters.BooleanFilter()
    tipo_competencia = django_filters.CharFilter(
        field_name='competencia__tipo'
    )

    class Meta:
        model = ItemPlan
        fields = ['plan', 'docente', 'completado']