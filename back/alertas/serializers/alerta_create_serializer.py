from rest_framework import serializers
from alertas.models.alerta_model import Alerta
from users.models.user import User


class AlertaCreateSerializer(serializers.ModelSerializer):
    """
    Campos de creación manual por admin/coordinador.

    Modos mutuamente excluyentes:
      - destinatario  → alerta individual
      - destinatario_rol → alerta para todos los usuarios activos de ese rol
    Si se envían ambos, destinatario tiene prioridad.
    """
    destinatario_rol = serializers.ChoiceField(
        choices=User.Rol.choices,
        required=False,
        write_only=True,
        help_text='Enviar a todos los usuarios activos de este rol.',
    )

    class Meta:
        model  = Alerta
        fields = [
            'tipo', 'descripcion', 'formato_alerta',
            'bloque_origen', 'destinatario', 'destinatario_rol',
        ]

    def validate(self, data):
        if (
            data.get('tipo') == Alerta.TipoAlerta.CONFLICTO
            and not data.get('bloque_origen')
        ):
            raise serializers.ValidationError(
                {'bloque_origen': 'Las alertas de conflicto requieren un bloque origen.'}
            )
        if not data.get('destinatario') and not data.get('destinatario_rol'):
            raise serializers.ValidationError(
                'Debes especificar un destinatario o un rol destino.'
            )
        return data