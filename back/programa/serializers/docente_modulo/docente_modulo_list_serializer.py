from rest_framework import serializers
from programa.models.docente_modulo_model import DocenteModulo


class DocenteModuloListSerializer(serializers.ModelSerializer):

    docente_nombre = serializers.CharField(
        source='docente.nombre', read_only=True
    )
    docente_email = serializers.EmailField(
        source='docente.email', read_only=True
    )
    modulo_nombre = serializers.CharField(
        source='modulo.nombre', read_only=True
    )

    class Meta:
        model = DocenteModulo
        fields = [
            'id', 'docente', 'docente_nombre', 'docente_email',
            'modulo', 'modulo_nombre',
            'fecha_asignacion', 'activo',
        ]