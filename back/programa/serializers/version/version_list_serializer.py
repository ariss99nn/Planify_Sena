from rest_framework import serializers
from programa.models.version_programa_model import VersionPrograma


class VersionListSerializer(serializers.ModelSerializer):

    programa_nombre = serializers.CharField(
        source='programa.nombre', read_only=True
    )
    total_modulos = serializers.SerializerMethodField()

    class Meta:
        model = VersionPrograma
        fields = [
            'id', 'numero', 'programa_nombre',
            'vigente', 'fecha_inicio', 'fecha_fin',
            'total_modulos',
        ]

    def get_total_modulos(self, obj):
        return obj.modulos.count()