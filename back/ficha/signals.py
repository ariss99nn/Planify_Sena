import logging
from django.db.models.signals import pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(pre_save, sender='ficha.Ficha')
def registrar_cambio_etapa(sender, instance, **kwargs):
    """
    Cuando Ficha.etapa cambia, crea un HistorialEtapa automáticamente.
    El usuario que hizo el cambio se pasa via instance._cambiado_por
    desde el serializer.
    """
    if not instance.pk:
        return

    try:
        anterior = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if anterior.etapa != instance.etapa:
        from ficha.models.historial_etapa_model import HistorialEtapa
        cambiado_por = getattr(instance, '_cambiado_por', None)
        HistorialEtapa.objects.create(
            ficha=instance,
            etapa_anterior=anterior.etapa,
            etapa_nueva=instance.etapa,
            trimestre=instance.trimestre,
            cambiado_por=cambiado_por,
        )
        logger.info(
            "Historial etapa creado: Ficha %s %s → %s",
            instance.codigo_ficha,
            anterior.etapa,
            instance.etapa,
        )