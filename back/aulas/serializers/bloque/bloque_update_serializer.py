from rest_framework import serializers
from aulas.models.bloque import Bloque


class BloqueUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bloque
        fields = [
            'nombre', 'piso', 'capacidad_maxima',
            'descripcion', 'imagen',
        ]

    def validate_capacidad_maxima(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'La capacidad máxima debe ser mayor a 0.'
            )
        return value

    def validate_piso(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'El número de pisos debe ser mayor a 0.'
            )
        return value