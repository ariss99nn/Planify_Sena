from rest_framework import serializers
from competencia.models.competencia_model import Competencia


class CompetenciaDetailSerializer(serializers.ModelSerializer):

    asignatura_nombre = serializers.CharField(
        source='asignatura.nombre', read_only=True
    )
    resultados = serializers.SerializerMethodField()

    class Meta:
        model = Competencia
        fields = [
            'id', 'asignatura', 'asignatura_nombre',
            'codigo', 'nombre', 'descripcion',
            'resultados',
            'created_at', 'updated_at',
        ]

    def get_resultados(self, obj):
        from competencia.serializers.resultado_aprendizaje.rap_list_serializer import (
            RAPListSerializer,
        )
        return RAPListSerializer(obj.resultados.all(), many=True).data