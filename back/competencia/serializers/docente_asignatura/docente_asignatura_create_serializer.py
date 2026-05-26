from rest_framework import serializers
from django.contrib.auth import get_user_model
from competencia.models.docente_asignatura_model import DocenteAsignatura

User = get_user_model()


class DocenteAsignaturaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocenteAsignatura
        fields = ['docente', 'asignatura', 'activo']

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
        if DocenteAsignatura.objects.filter(
            docente=data['docente'],
            asignatura=data['asignatura'],
        ).exists():
            raise serializers.ValidationError(
                'Este docente ya está asignado a esta asignatura.'
            )
        return data