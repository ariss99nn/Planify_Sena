from rest_framework import serializers
from aulas.models.aula import Aula


class AulaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aula
        fields = [
            'codigo_aula', 'capacidad', 'tipo_aula',
            'estado', 'bloque', 'descripcion',
            'imagen', 'equipamiento',
        ]

    def validate_capacidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La capacidad debe ser mayor a 0.')
        return value

    def validate_codigo_aula(self, value):
        value = value.upper().strip()
        # CORRECCIÓN: validar unicidad después de normalizar para devolver 400
        # en lugar de dejar que la BD falle con un IntegrityError (500).
        qs = Aula.objects.filter(codigo_aula=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Ya existe un aula con este código.')
        return value