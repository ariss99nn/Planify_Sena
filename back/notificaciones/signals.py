from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender='alertas.Alerta')
def enviar_alerta_websocket(sender, instance, created, **kwargs):
    """
    Al crear una alerta, la envía via WebSocket al destinatario
    y si es conflicto también al grupo de managers.
    """
    if not created:
        return

    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.warning("Channel layer no configurado — alerta no enviada por WS")
        return

    payload = {
        'id': instance.pk,
        'tipo_alerta': instance.tipo,
        'descripcion': instance.descripcion,
        'fecha': instance.fecha_creacion.isoformat(),
    }

    # Enviar al destinatario personal
    if instance.destinatario_id:
        group_name = f'alertas_user_{instance.destinatario_id}'
        try:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {'type': 'alerta.nueva', **payload},
            )
        except Exception as e:
            logger.error("Error enviando WS a %s: %s", group_name, e)

    # Si es conflicto, notificar también a managers
    from alertas.models.alerta_model import Alerta
    if instance.tipo == Alerta.TipoAlerta.CONFLICTO:
        try:
            async_to_sync(channel_layer.group_send)(
                'alertas_managers',
                {
                    'type': 'alerta.conflicto',
                    'descripcion': instance.descripcion,
                    'bloque_id': instance.bloque_origen_id,
                    'fecha': instance.fecha_creacion.isoformat(),
                },
            )
        except Exception as e:
            logger.error("Error enviando WS conflicto a managers: %s", e)