from rest_framework import serializers
from programa.models.modulo import Modulo


class ModuloListSerializer(serializers.ModelSerializer):

    version_numero = serializers.IntegerField(
        source='version.numero', read_only=True
    )
    estado_display = serializers.CharField(
        source='get_estado_display', read_only=True
    )
    total_horas = serializers.IntegerField(read_only=True)
    total_asignaturas = serializers.SerializerMethodField()

    class Meta:
        model = Modulo
        fields = [
            'id', 'nombre', 'orden',
            'version_numero', 'estado', 'estado_display',
            'horas_lectivas', 'horas_practicas', 'total_horas',
            'total_asignaturas',
        ]

    def get_total_asignaturas(self, obj):
        return obj.asignaturas.count()