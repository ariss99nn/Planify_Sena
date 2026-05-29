import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender='bhorario.BloqueHorario')
def detectar_conflictos_horario(sender, instance, created, **kwargs):
    """
    Al crear un BloqueHorario detecta solapamientos y genera UNA sola
    alerta consolidada por docente. También notifica a coordinadores/admins.
    """
    if not created or not instance.docente_id:
        return

    from alertas.models.alerta_model import Alerta
    from users.models.user import User

    conflictos = sender.objects.filter(
        dia_semana=instance.dia_semana,
        docente=instance.docente,
        hora_inicio__lt=instance.hora_fin,
        hora_fin__gt=instance.hora_inicio,
    ).exclude(pk=instance.pk)

    if not conflictos.exists():
        return

    ids_conflicto = ', '.join(str(c.pk) for c in conflictos)
    descripcion_base = (
        f"Conflicto de horario: el docente {instance.docente} "
        f"tiene bloques solapados el {instance.get_dia_semana_display()} "
        f"{instance.hora_inicio:%H:%M} – {instance.hora_fin:%H:%M}. "
        f"Bloques en conflicto: #{ids_conflicto}."
    )

    logger.warning(
        "Conflicto detectado — Docente %s | bloque nuevo: %s | solapados: %s",
        instance.docente,
        instance.pk,
        ids_conflicto,
    )

    # Alerta para el docente
    Alerta.objects.create(
        tipo=Alerta.TipoAlerta.CONFLICTO,
        descripcion=descripcion_base,
        bloque_origen=instance,
        destinatario=instance.docente.user,
        formato_alerta=Alerta.FormatoAlerta.APP,
    )

    # Alerta para cada coordinador/admin activo
    gestores = User.objects.filter(
        rol__in=[User.Rol.COORDINADOR, User.Rol.ADMIN],
        is_active=True,
    )
    alertas_gestores = [
        Alerta(
            tipo=Alerta.TipoAlerta.CONFLICTO,
            descripcion=descripcion_base,
            bloque_origen=instance,
            destinatario=gestor,
            formato_alerta=Alerta.FormatoAlerta.APP,
        )
        for gestor in gestores
    ]
    if alertas_gestores:
        Alerta.objects.bulk_create(alertas_gestores)