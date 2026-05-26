from rest_framework import serializers
from aulas.models.aula import Aula


class AulaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aula
        fields = [
            'capacidad', 'tipo_aula', 'estado',
            'bloque', 'descripcion', 'imagen', 'equipamiento',
        ]

    def validate_capacidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La capacidad debe ser mayor a 0.')
        return value