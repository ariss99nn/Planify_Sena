from rest_framework import serializers
from django.contrib.auth import get_user_model
from ficha.models.ficha_estudiante_model import FichaEstudiante

User = get_user_model()


class FichaEstudianteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FichaEstudiante
        fields = ['ficha', 'estudiante', 'es_cadena']

    def validate_estudiante(self, user):
        if user.rol != User.Rol.ESTUDIANTE:
            raise serializers.ValidationError(
                'El usuario debe tener rol ESTUDIANTE.'
            )
        if not user.estado:
            raise serializers.ValidationError(
                'No se puede asignar un estudiante inactivo.'
            )
        return user

    def validate(self, data):
        ficha = data.get('ficha')
        estudiante = data.get('estudiante')
        es_cadena = data.get('es_cadena', False)

        # Validar que no esté ya en esta ficha
        if FichaEstudiante.objects.filter(
            ficha=ficha, estudiante=estudiante
        ).exists():
            raise serializers.ValidationError(
                'Este estudiante ya está asignado a esta ficha.'
            )

        # Si no es cadena, validar que no tenga otra ficha activa
        if not es_cadena:
            activas = FichaEstudiante.objects.filter(
                estudiante=estudiante,
                activo=True,
                es_cadena=False,
            )
            if activas.exists():
                ficha_activa = activas.first().ficha.codigo_ficha
                raise serializers.ValidationError(
                    f'El estudiante ya tiene una ficha activa ({ficha_activa}). '
                    f'Use reasignación para cambiarlo, o marque como cadena de formación.'
                )

        return data