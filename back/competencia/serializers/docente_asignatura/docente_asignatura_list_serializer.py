from rest_framework import serializers
from competencia.models.docente_asignatura_model import DocenteAsignatura


class DocenteAsignaturaListSerializer(serializers.ModelSerializer):

    docente_nombre = serializers.CharField(
        source='docente.nombre', read_only=True
    )
    docente_email = serializers.EmailField(
        source='docente.email', read_only=True
    )
    asignatura_nombre = serializers.CharField(
        source='asignatura.nombre', read_only=True
    )

    class Meta:
        model = DocenteAsignatura
        fields = [
            'id', 'docente', 'docente_nombre', 'docente_email',
            'asignatura', 'asignatura_nombre',
            'fecha_asignacion', 'activo',
        ]