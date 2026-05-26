from rest_framework import serializers
from alertas.models.alerta_model import Alerta


class AlertaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alerta
        fields = [
            'tipo', 'descripcion', 'formato_alerta',
            'bloque_origen', 'destinatario',
        ]

    def validate(self, data):
        if (
            data.get('tipo') == Alerta.TipoAlerta.CONFLICTO
            and not data.get('bloque_origen')
        ):
            raise serializers.ValidationError(
                'Las alertas de conflicto deben tener un bloque origen.'
            )
        return data