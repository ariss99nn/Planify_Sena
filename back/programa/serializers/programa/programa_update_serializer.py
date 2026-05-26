from rest_framework import serializers
from programa.models.programa_model import Programa


class ProgramaUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Programa
        fields = [
            'nombre', 'descripcion', 'nivel',
            'horas_lectivas', 'horas_practicas', 'estado',
        ]

    def validate(self, data):
        horas_lectivas = data.get(
            'horas_lectivas',
            self.instance.horas_lectivas if self.instance else 0
        )
        horas_practicas = data.get(
            'horas_practicas',
            self.instance.horas_practicas if self.instance else 0
        )
        if horas_lectivas <= 0:
            raise serializers.ValidationError(
                {'horas_lectivas': 'Las horas lectivas deben ser mayores a 0.'}
            )
        if horas_practicas < 0:
            raise serializers.ValidationError(
                {'horas_practicas': 'Las horas prácticas no pueden ser negativas.'}
            )
        return data