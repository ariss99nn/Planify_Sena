from django.db import transaction
from rest_framework import serializers
from docentes.models.docente import Docente


class DocenteDeactivateSerializer(serializers.ModelSerializer):
    """
    Desactiva el perfil docente y su usuario asociado de forma atómica.
    Ningún registro se elimina — quedan históricos para reportes.
    """
    confirmacion = serializers.BooleanField(write_only=True)

    class Meta:
        model = Docente
        fields = ['confirmacion']

    def validate_confirmacion(self, value):
        if value is not True:
            raise serializers.ValidationError(
                "Debe confirmar la desactivación del docente."
            )
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.estado = False
        instance.save(update_fields=['estado'])

        instance.user.estado = False
        instance.user.save(update_fields=['estado'])

        return instance