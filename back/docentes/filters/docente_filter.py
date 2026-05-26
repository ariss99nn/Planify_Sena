import django_filters
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from docentes.models.docente import Docente


class DocentePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class DocenteFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Búsqueda general',
    )
    estado = django_filters.BooleanFilter()
    especialidad = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Especialidad',
    )

    class Meta:
        model = Docente
        fields = ['estado', 'especialidad']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(user__nombre__icontains=value) |
            Q(user__email__icontains=value) |
            Q(especialidad__icontains=value)
        )