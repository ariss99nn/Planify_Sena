from rest_framework import serializers
from competencia.models.competencia_model import Competencia


class CompetenciaListSerializer(serializers.ModelSerializer):

    asignatura_nombre = serializers.CharField(
        source='asignatura.nombre', read_only=True
    )
    total_resultados = serializers.SerializerMethodField()

    class Meta:
        model = Competencia
        fields = [
            'id', 'codigo', 'nombre',
            'asignatura_nombre', 'total_resultados',
        ]

    def get_total_resultados(self, obj):
        return obj.resultados.count()