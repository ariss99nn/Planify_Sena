from rest_framework import serializers
from competencia.models.docente_asignatura_model import DocenteAsignatura


class DocenteAsignaturaUpdateSerializer(serializers.ModelSerializer):
    """Solo permite activar o desactivar la asignación."""

    class Meta:
        model = DocenteAsignatura
        fields = ['activo']