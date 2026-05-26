from rest_framework import serializers
from competencia.models.resultado_aprendizaje_model import ResultadoAprendizaje


class RAPUpdateSerializer(serializers.ModelSerializer):
    """No permite cambiar competencia ni código."""

    class Meta:
        model = ResultadoAprendizaje
        fields = ['descripcion', 'criterios_evaluacion']