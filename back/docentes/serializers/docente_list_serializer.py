from rest_framework import serializers
from docentes.models.docente import Docente
from docentes.serializers.base_serializer import BaseDocenteSerializer


class DocenteListSerializer(BaseDocenteSerializer):

    nombre = serializers.CharField(source='user.nombre', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar = serializers.ImageField(source='user.imagen', read_only=True)

    class Meta:
        model = Docente
        fields = [
            'id',
            'nombre',
            'email',
            'avatar',       # foto de perfil del User
            'imagen',       # foto institucional del Docente
            'especialidad',
            'horas_max_semanales',
            'estado',
        ]