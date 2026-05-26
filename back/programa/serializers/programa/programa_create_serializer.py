from rest_framework import serializers
from programa.models.programa_model import Programa


class ProgramaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Programa
        fields = [
            'nombre', 'descripcion', 'nivel',
            'horas_lectivas', 'horas_practicas', 'estado',
        ]

    def validate(self, data):
        if data.get('horas_lectivas', 0) <= 0:
            raise serializers.ValidationError(
                {'horas_lectivas': 'Las horas lectivas deben ser mayores a 0.'}
            )
        if data.get('horas_practicas', 0) < 0:
            raise serializers.ValidationError(
                {'horas_practicas': 'Las horas prácticas no pueden ser negativas.'}
            )
        return data