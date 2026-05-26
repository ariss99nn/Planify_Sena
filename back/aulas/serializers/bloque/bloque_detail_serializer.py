from rest_framework import serializers
from aulas.models.bloque import Bloque


class BloqueDetailSerializer(serializers.ModelSerializer):

    # MEJORA: este campo dispara una query extra por cada instancia serializada
    # (problema N+1). Para evitarlo, anotar el queryset desde el ViewSet:
    #
    #   from django.db.models import Count
    #   queryset = Bloque.objects.annotate(total_aulas=Count('aulas'))
    #
    # Y luego usar un SerializerMethodField o un simple IntegerField(read_only=True)
    # apuntando a la anotación. Mientras el volumen sea bajo, el impacto es mínimo,
    # pero conviene resolverlo antes de escalar.
    total_aulas = serializers.SerializerMethodField()

    class Meta:
        model = Bloque
        fields = [
            'id', 'nombre', 'piso', 'capacidad_maxima',
            'descripcion', 'imagen', 'total_aulas',
        ]

    def get_total_aulas(self, obj):
        # Usa la anotación si existe; cae a la query si no (retrocompatible).
        if hasattr(obj, 'total_aulas_annotated'):
            return obj.total_aulas_annotated
        return obj.aulas.count()