import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

logger = logging.getLogger(__name__)

_MANAGERS_GROUP = 'alertas_managers'


def _send_to_group(channel_layer, group: str, message: dict):
    from asgiref.sync import async_to_sync
    try:
        async_to_sync(channel_layer.group_send)(group, message)
    except Exception as exc:
        logger.error("WS group_send '%s' falló: %s", group, exc)


@receiver(post_save, sender='alertas.Alerta')
def enviar_alerta_websocket(sender, instance, created, **kwargs):
    if not created:
        return

    from channels.layers import get_channel_layer
    from alertas.models.alerta_model import Alerta

    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.warning("Channel layer no configurado — WS omitido")
        return

    payload = {
        'id':          instance.pk,
        'tipo_alerta': instance.tipo,
        'descripcion': instance.descripcion,
        'fecha':       instance.fecha_creacion.isoformat(),
    }

    def _dispatch():
        # Destinatario personal
        if instance.destinatario_id:
            _send_to_group(
                channel_layer,
                f'alertas_user_{instance.destinatario_id}',
                {'type': 'alerta_nueva', **payload},
            )

        # Conflictos → grupo managers
        if instance.tipo == Alerta.TipoAlerta.CONFLICTO:
            _send_to_group(
                channel_layer,
                _MANAGERS_GROUP,
                {
                    'type':        'alerta_conflicto',
                    'descripcion': instance.descripcion,
                    'bloque_id':   instance.bloque_origen_id,
                    'fecha':       instance.fecha_creacion.isoformat(),
                },
            )

    # on_commit garantiza que el WS solo se envía si la transacción persiste
    transaction.on_commit(_dispatch)