from rest_framework import serializers
from aulas.models.aula import Aula


class AulaEstadoSerializer(serializers.ModelSerializer):
    """
    Para DOCENTE: solo puede cambiar el estado del aula.
    No puede modificar capacidad, tipo, bloque ni equipamiento.
    """

    class Meta:
        model = Aula
        fields = ['estado']

    # CORRECCIÓN: eliminada validate_estado — DRF ya valida automáticamente
    # que el valor esté dentro de los choices del campo. La validación manual
    # era redundante (dead code).