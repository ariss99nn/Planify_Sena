from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from ficha.models.reasignacion_ficha_model import ReasignacionFicha
from ficha.models.ficha_estudiante_model import FichaEstudiante

User = get_user_model()


class ReasignacionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReasignacionFicha
        fields = [
            'estudiante', 'ficha_origen',
            'ficha_destino', 'motivo',
        ]

    def validate_estudiante(self, user):
        if user.rol != User.Rol.ESTUDIANTE:
            raise serializers.ValidationError(
                'El usuario debe tener rol ESTUDIANTE.'
            )
        return user

    def validate(self, data):
        estudiante = data['estudiante']
        ficha_origen = data['ficha_origen']
        ficha_destino = data['ficha_destino']

        if ficha_origen == ficha_destino:
            raise serializers.ValidationError(
                'La ficha de origen y destino no pueden ser la misma.'
            )

        try:
            self._relacion_origen = FichaEstudiante.objects.get(
                estudiante=estudiante,
                ficha=ficha_origen,
                activo=True,
            )
        except FichaEstudiante.DoesNotExist:
            raise serializers.ValidationError(
                f'El estudiante no está activo en la ficha '
                f'{ficha_origen.codigo_ficha}.'
            )

        if not ficha_destino.estado:
            raise serializers.ValidationError(
                f'La ficha destino {ficha_destino.codigo_ficha} no está activa.'
            )

        if FichaEstudiante.objects.filter(
            estudiante=estudiante,
            ficha=ficha_destino,
            activo=True,
        ).exists():
            raise serializers.ValidationError(
                f'El estudiante ya está activo en la ficha destino '
                f'{ficha_destino.codigo_ficha}.'
            )

        return data

    @transaction.atomic
    def save(self, **kwargs):
        request = self.context.get('request')
        realizado_por = request.user if request else None
        hoy = timezone.now().date()

        estudiante = self.validated_data['estudiante']
        ficha_origen = self.validated_data['ficha_origen']
        ficha_destino = self.validated_data['ficha_destino']
        motivo = self.validated_data['motivo']

        # 1 — Desactivar en origen con motivo REASIGNADO
        self._relacion_origen.activo = False
        self._relacion_origen.fecha_retiro = hoy
        self._relacion_origen.motivo_retiro = FichaEstudiante.MotivoRetiro.REASIGNADO
        self._relacion_origen.save(
            update_fields=['activo', 'fecha_retiro', 'motivo_retiro']
        )

        # 2 — Crear en destino
        FichaEstudiante.objects.create(
            ficha=ficha_destino,
            estudiante=estudiante,
            activo=True,
            es_cadena=self._relacion_origen.es_cadena,
        )

        # 3 — Registrar reasignación
        reasignacion = ReasignacionFicha.objects.create(
            estudiante=estudiante,
            ficha_origen=ficha_origen,
            ficha_destino=ficha_destino,
            motivo=motivo,
            realizado_por=realizado_por,
        )

        return reasignacion