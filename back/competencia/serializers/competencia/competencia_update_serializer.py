from rest_framework import serializers
from competencia.models.competencia_model import Competencia


class CompetenciaUpdateSerializer(serializers.ModelSerializer):
    """No permite cambiar la asignatura ni el código."""

    class Meta:
        model = Competencia
        fields = ['nombre', 'descripcion']