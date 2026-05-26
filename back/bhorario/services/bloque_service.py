# bhorario/services/bloque_service.py
import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from bhorario.models.bloque_horario_model import BloqueHorario

logger = logging.getLogger(__name__)


class ColisionError(Exception):
    """Error semántico de colisión de horario."""
    pass


class BloqueHorarioService:

    @staticmethod
    @transaction.atomic
    def crear_bloque(datos: dict) -> BloqueHorario:
        """
        Creación atómica con tres capas de protección:
        1. select_for_update() — lock de filas candidatas a conflicto
        2. clean() del modelo — validación de negocio
        3. EXCLUDE constraint PostgreSQL — garantía absoluta en DB
        """
        dia = datos.get('dia_semana')
        h_inicio = datos.get('hora_inicio')
        h_fin = datos.get('hora_fin')
        docente = datos.get('docente')
        aula = datos.get('aula')
        ficha = datos.get('ficha')

        # Capa 1 — lock preventivo
        qs_base = BloqueHorario.objects.select_for_update().filter(
            dia_semana=dia,
            hora_inicio__lt=h_fin,
            hora_fin__gt=h_inicio,
        )
        if docente:
            qs_base.filter(docente=docente).exists()
        if aula:
            qs_base.filter(aula=aula).exists()
        if ficha:
            qs_base.filter(ficha=ficha).exists()

        # Capa 2 — validación de negocio
        bloque = BloqueHorario(**datos)
        try:
            bloque.full_clean()
        except ValidationError as e:
            raise ColisionError(str(e)) from e

        bloque.save()
        logger.info(
            "Bloque creado: %s — Docente: %s | Aula: %s | Ficha: %s",
            bloque, docente, aula, ficha,
        )
        return bloque

    @staticmethod
    @transaction.atomic
    def actualizar_bloque(bloque: BloqueHorario, datos: dict) -> BloqueHorario:
        for campo, valor in datos.items():
            setattr(bloque, campo, valor)
        try:
            bloque.full_clean()
        except ValidationError as e:
            raise ColisionError(str(e)) from e
        bloque.save()
        return bloque

    @staticmethod
    def verificar_disponibilidad(
        dia: str,
        hora_inicio,
        hora_fin,
        docente=None,
        aula=None,
        ficha=None,
        excluir_pk=None,
    ) -> dict:
        """
        Verifica disponibilidad sin crear nada.
        Útil para el frontend antes de mostrar el formulario de creación.
        """
        qs = BloqueHorario.objects.filter(
            dia_semana=dia,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio,
        )
        if excluir_pk:
            qs = qs.exclude(pk=excluir_pk)

        resultado = {
            'docente_disponible': True,
            'aula_disponible': True,
            'ficha_disponible': True,
            'conflictos': [],
        }

        if docente and qs.filter(docente=docente).exists():
            resultado['docente_disponible'] = False
            resultado['conflictos'].append(
                f'Docente {docente} no disponible el {dia} {hora_inicio}-{hora_fin}'
            )

        if aula and qs.filter(aula=aula).exists():
            resultado['aula_disponible'] = False
            resultado['conflictos'].append(
                f'Aula {aula} no disponible el {dia} {hora_inicio}-{hora_fin}'
            )

        if ficha and qs.filter(ficha=ficha).exists():
            resultado['ficha_disponible'] = False
            resultado['conflictos'].append(
                f'Ficha {ficha} no disponible el {dia} {hora_inicio}-{hora_fin}'
            )

        return resultado