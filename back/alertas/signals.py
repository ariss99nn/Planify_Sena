import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender='bhorario.BloqueHorario')
def detectar_conflictos_horario(sender, instance, created, **kwargs):
    """
    Al crear o modificar un BloqueHorario, el sistema detecta conflictos
    y genera alertas automáticamente para el docente y para IsManager.
    """
    if not created:
        return

    from alertas.models.alerta_model import Alerta

    # Conflicto de docente
    if instance.docente_id:
        from bhorario.models.bloque_horario_model import BloqueHorario
        conflictos = BloqueHorario.objects.filter(
            dia_semana=instance.dia_semana,
            docente=instance.docente,
            hora_inicio__lt=instance.hora_fin,
            hora_fin__gt=instance.hora_inicio,
        ).exclude(pk=instance.pk)

        for conflicto in conflictos:
            Alerta.objects.create(
                tipo=Alerta.TipoAlerta.CONFLICTO,
                descripcion=(
                    f"Conflicto de horario: docente {instance.docente} "
                    f"tiene bloques solapados el {instance.get_dia_semana_display()} "
                    f"{instance.hora_inicio} - {instance.hora_fin}."
                ),
                bloque_origen=instance,
                destinatario=instance.docente.user,
                formato_alerta=Alerta.FormatoAlerta.APP,
            )
            logger.warning(
                "Conflicto detectado: Docente %s — bloques %s y %s",
                instance.docente,
                instance.pk,
                conflicto.pk,
            )