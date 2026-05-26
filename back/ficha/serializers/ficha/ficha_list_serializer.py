from rest_framework import serializers
from ficha.models.ficha_model import Ficha


class FichaListSerializer(serializers.ModelSerializer):

    programa_nombre = serializers.CharField(
        source='version.programa.nombre', read_only=True
    )
    version_numero = serializers.IntegerField(
        source='version.numero', read_only=True
    )
    jornada_display = serializers.CharField(
        source='get_jornada_display', read_only=True
    )
    etapa_display = serializers.CharField(
        source='get_etapa_display', read_only=True
    )
    numero_estudiantes_real = serializers.IntegerField(read_only=True)
    jefe_grupo_nombre = serializers.CharField(
        source='jefe_grupo.nombre', read_only=True, default=None
    )

    class Meta:
        model = Ficha
        fields = [
            'id', 'codigo_ficha',
            'programa_nombre', 'version_numero',
            'jornada', 'jornada_display',
            'etapa', 'etapa_display',
            'trimestre', 'estado',
            'cadena_formacion',
            'numero_estudiantes_estimado',
            'numero_estudiantes_real',
            'jefe_grupo_nombre',
            'fecha_inicio', 'fecha_finalizacion',
        ]

        # PRIORIDAD A LAS FICHAS QUE IENE INICIO DE ETAPA LECTIVA MAS RECIENTE A DIFERENCIA DE LAS QUE YA TIENE MAS TRIMESTES