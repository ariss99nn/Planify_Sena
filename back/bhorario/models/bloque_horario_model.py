# bhorario/models/bloque_horario_model.py
from django.db import models
from django.core.exceptions import ValidationError


class BloqueHorario(models.Model):

    class DiaSemana(models.TextChoices):
        LUNES    = 'LUNES',    'Lunes'
        MARTES   = 'MARTES',   'Martes'
        MIERCOLES = 'MIERCOLES', 'Miércoles'
        JUEVES   = 'JUEVES',   'Jueves'
        VIERNES  = 'VIERNES',  'Viernes'
        SABADO   = 'SABADO',   'Sábado'
        DOMINGO  = 'DOMINGO',  'Domingo'

    class Jornada(models.TextChoices):
        MANANA = 'MANANA', 'Mañana'
        TARDE  = 'TARDE',  'Tarde'
        NOCHE  = 'NOCHE',  'Noche'
        MIXTA  = 'MIXTA',  'Mixta'

    dia_semana = models.CharField(
        max_length=10, choices=DiaSemana.choices, db_index=True,
    )
    hora_inicio = models.TimeField()
    hora_fin    = models.TimeField()
    jornada = models.CharField(
        max_length=10, choices=Jornada.choices, db_index=True,
    )
    es_recurrente = models.BooleanField(
        default=True,
        help_text='True = aplica cada semana. False = solo fecha_especifica.',
    )
    fecha_especifica = models.DateField(
        null=True, blank=True,
        help_text='Solo si es_recurrente=False.',
    )
    aula = models.ForeignKey(
        'aulas.Aula', on_delete=models.PROTECT,
        related_name='bloques_horario', null=True, blank=True,
    )
    docente = models.ForeignKey(
        'docentes.Docente', on_delete=models.PROTECT,
        related_name='bloques_horario', null=True, blank=True,
    )
    ficha = models.ForeignKey(
        'ficha.Ficha', on_delete=models.PROTECT,
        related_name='bloques_horario', null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Bloque de horario'
        verbose_name_plural = 'Bloques de horario'
        ordering            = ['dia_semana', 'hora_inicio']
        indexes = [
            models.Index(fields=['dia_semana', 'jornada']),
            models.Index(fields=['dia_semana', 'hora_inicio']),
            models.Index(fields=['es_recurrente', 'fecha_especifica']),
            models.Index(
                fields=['dia_semana', 'docente', 'hora_inicio', 'hora_fin'],
                name='idx_bhorario_docente_colision',
            ),
            models.Index(
                fields=['dia_semana', 'aula', 'hora_inicio', 'hora_fin'],
                name='idx_bhorario_aula_colision',
            ),
            models.Index(
                fields=['dia_semana', 'ficha', 'hora_inicio', 'hora_fin'],
                name='idx_bhorario_ficha_colision',
            ),
        ]

    def __str__(self):
        return (
            f"{self.get_dia_semana_display()} "
            f"{self.hora_inicio} - {self.hora_fin}"
        )

    def clean(self):
        if self.hora_inicio and self.hora_fin:
            if self.hora_inicio >= self.hora_fin:
                raise ValidationError({
                    'hora_fin': 'La hora de fin debe ser mayor a la hora de inicio.'
                })
        if not self.es_recurrente and not self.fecha_especifica:
            raise ValidationError({
                'fecha_especifica': (
                    'Debe indicar la fecha específica si el bloque no es recurrente.'
                )
            })
        if self.es_recurrente and self.fecha_especifica:
            raise ValidationError({
                'fecha_especifica': (
                    'Un bloque recurrente no debe tener fecha específica.'
                )
            })
        self._validar_conflicto_docente()
        self._validar_conflicto_aula()
        self._validar_conflicto_ficha()

    def _get_base_qs(self):
        """
        QS base de bloques solapados en el mismo día/hora.
        CORRECCIÓN: considera correctamente recurrentes vs fecha_especifica.
        Un recurrente solo colisiona con otros recurrentes del mismo día.
        Un one-shot solo colisiona con recurrentes del mismo día Y con
        one-shots de la misma fecha_especifica.
        """
        qs = BloqueHorario.objects.filter(
            dia_semana=self.dia_semana,
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio,
        ).exclude(pk=self.pk)

        if self.es_recurrente:
            # Recurrente colisiona con otros recurrentes
            return qs.filter(es_recurrente=True)
        else:
            # One-shot colisiona con recurrentes Y con one-shots de la misma fecha
            from django.db.models import Q
            return qs.filter(
                Q(es_recurrente=True) |
                Q(es_recurrente=False, fecha_especifica=self.fecha_especifica)
            )

    def _validar_conflicto_docente(self):
        if self.docente_id and self._get_base_qs().filter(
            docente_id=self.docente_id
        ).exists():
            raise ValidationError(
                'El docente ya tiene un bloque asignado en ese horario.'
            )

    def _validar_conflicto_aula(self):
        if self.aula_id and self._get_base_qs().filter(
            aula_id=self.aula_id
        ).exists():
            raise ValidationError(
                'El aula ya tiene un bloque asignado en ese horario.'
            )

    def _validar_conflicto_ficha(self):
        if self.ficha_id and self._get_base_qs().filter(
            ficha_id=self.ficha_id
        ).exists():
            raise ValidationError(
                'La ficha ya tiene un bloque asignado en ese horario.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)