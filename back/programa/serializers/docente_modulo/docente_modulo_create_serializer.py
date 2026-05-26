from rest_framework import serializers
from django.contrib.auth import get_user_model
from programa.models.docente_modulo_model import DocenteModulo

User = get_user_model()


class DocenteModuloCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocenteModulo
        fields = ['docente', 'modulo', 'activo']

    def validate_docente(self, user):
        if user.rol != User.Rol.DOCENTE:
            raise serializers.ValidationError(
                'El usuario debe tener rol DOCENTE.'
            )
        if not user.estado:
            raise serializers.ValidationError(
                'No se puede asignar un usuario inactivo.'
            )
        return user

    def validate(self, data):
        if DocenteModulo.objects.filter(
            docente=data['docente'],
            modulo=data['modulo'],
        ).exists():
            raise serializers.ValidationError(
                'Este docente ya está asignado a este módulo.'
            )
        return data