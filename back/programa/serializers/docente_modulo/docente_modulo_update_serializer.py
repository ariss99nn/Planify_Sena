from rest_framework import serializers
from programa.models.docente_modulo_model import DocenteModulo


class DocenteModuloUpdateSerializer(serializers.ModelSerializer):
    """
    Solo permite activar o desactivar la asignación.
    No permite cambiar docente ni módulo — crear una nueva asignación para eso.
    """

    class Meta:
        model = DocenteModulo
        fields = ['activo']