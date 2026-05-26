from rest_framework import serializers
from docentes.models.docente import Docente
from docentes.serializers.base_serializer import BaseDocenteSerializer
from users.serializers.user_base_serializer import UserBaseSerializer


class DocenteDetailSerializer(BaseDocenteSerializer):
    """
    Detalle completo: datos del User anidados + campos propios del Docente.
    user.imagen = avatar de perfil.
    imagen = foto institucional del docente.
    """
    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = Docente
        fields = [
            'id',
            'user',
            'especialidad',
            'horas_max_semanales',
            'estado',
            'imagen',
        ]