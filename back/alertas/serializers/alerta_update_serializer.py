from rest_framework import serializers
from django.utils import timezone
from alertas.models.alerta_model import Alerta


class AlertaUpdateSerializer(serializers.ModelSerializer):
    """
    Permite cambiar estado de la alerta.
    Al marcar como LEIDA registra fecha_lectura automáticamente.
    """

    class Meta:
        model = Alerta
        fields = ['estado', 'formato_alerta']

    def update(self, instance, validated_data):
        nuevo_estado = validated_data.get('estado', instance.estado)
        if (
            nuevo_estado == Alerta.EstadoAlerta.LEIDA
            and instance.estado != Alerta.EstadoAlerta.LEIDA
        ):
            instance.fecha_lectura = timezone.now()
        return super().update(instance, validated_data)