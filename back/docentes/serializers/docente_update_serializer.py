from docentes.models.docente import Docente
from docentes.serializers.base_serializer import BaseDocenteSerializer


class DocenteUpdateSerializer(BaseDocenteSerializer):
    """
    Actualiza campos del perfil docente.
    user_id no es modificable después de la creación.
    """

    class Meta:
        model = Docente
        fields = [
            'especialidad',
            'horas_max_semanales',
            'estado',
            'imagen',
        ]