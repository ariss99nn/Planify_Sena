from rest_framework import serializers
from django.contrib.auth import get_user_model
from ficha.models.ficha_model import Ficha

User = get_user_model()


class FichaUpdateSerializer(serializers.ModelSerializer):
    """
    Actualización general de ficha.
    El cambio de etapa tiene su propio serializer (FichaEtapaUpdateSerializer)
    para garantizar que se registre el historial correctamente.
    """

    class Meta:
        model = Ficha
        fields = [
            'jornada', 'numero_estudiantes_estimado',
            'horas_semanales_objetivo', 'trimestre',
            'estado', 'cadena_formacion',
            'jefe_grupo', 'fecha_inicio', 'fecha_finalizacion',
        ]

    def validate_jefe_grupo(self, user):
        if user is None:
            return user
        if user.rol != User.Rol.DOCENTE:
            raise serializers.ValidationError(
                'El jefe de grupo debe tener rol DOCENTE.'
            )
        if not user.estado:
            raise serializers.ValidationError(
                'El jefe de grupo no puede ser un usuario inactivo.'
            )
        return user

    def validate_numero_estudiantes_estimado(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'El número de estudiantes estimado debe ser mayor a 0.'
            )
        return value

    def validate(self, data):
        fecha_inicio = data.get(
            'fecha_inicio',
            self.instance.fecha_inicio if self.instance else None,
        )
        fecha_fin = data.get('fecha_finalizacion')
        if fecha_fin and fecha_inicio and fecha_fin < fecha_inicio:
            raise serializers.ValidationError({
                'fecha_finalizacion': (
                    'La fecha de finalización no puede ser '
                    'anterior a la fecha de inicio.'
                )
            })
        return data