from rest_framework import serializers
from competencia.models.competencia_model import Competencia


class CompetenciaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competencia
        fields = ['asignatura', 'codigo', 'nombre', 'descripcion']

    def validate_codigo(self, value):
        value = value.upper().strip()
        if Competencia.objects.filter(codigo=value).exists():
            raise serializers.ValidationError(
                f'Ya existe una competencia con el código "{value}".'
            )
        return value