from rest_framework import serializers
from aulas.models.equipamiento import Equipamiento


class EquipamientoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipamiento
        fields = [
            'nombre', 'descripcion', 'cantidad',
            'numero_serie', 'fecha_adquisicion',
            'estado', 'imagen',
        ]

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La cantidad debe ser mayor a 0.')
        return value