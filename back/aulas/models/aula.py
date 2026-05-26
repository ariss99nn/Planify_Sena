# aulas/models/aula.py
from django.db import models
from django.core.exceptions import ValidationError
from aulas.models.bloque import Bloque
from aulas.models.equipamiento import Equipamiento
from users.validators import validate_imagen_5mb


class Aula(models.Model):

    class TipoAula(models.TextChoices):
        LABORATORIO = 'LAB', 'Laboratorio'
        TEORICA     = 'TEO', 'Teórica'
        SISTEMAS    = 'SIS', 'Sistemas de Información'
        OTRO        = 'OTR', 'Otro'

    class Estado(models.TextChoices):
        ACTIVA        = 'ACT',  'Activa'
        MANTENIMIENTO = 'MANT', 'Mantenimiento'
        INACTIVA      = 'INAC', 'Inactiva'

    codigo_aula = models.CharField(max_length=10, unique=True, db_index=True)
    capacidad = models.PositiveIntegerField()
    tipo_aula = models.CharField(
        max_length=10,
        choices=TipoAula.choices,
    )
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ACTIVA,
    )
    bloque = models.ForeignKey(
        Bloque,
        on_delete=models.PROTECT,
        related_name='aulas',
    )
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(
        upload_to='aulas/',
        null=True,
        blank=True,
        validators=[validate_imagen_5mb],
    )
    equipamiento = models.ManyToManyField(
        Equipamiento,
        blank=True,
        related_name='aulas',
    )

    class Meta:
        verbose_name        = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering            = ['bloque', 'codigo_aula']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['tipo_aula']),
            models.Index(fields=['bloque', 'estado']),   # MEJORA: filtrar aulas activas por bloque
        ]

    def __str__(self):
        return f"{self.codigo_aula} — {self.bloque.nombre}"

    def clean(self):
        if self.capacidad is not None and self.capacidad <= 0:
            raise ValidationError({'capacidad': 'La capacidad debe ser mayor a 0.'})
        # CORRECCIÓN: un aula de un bloque inactivo no debería estar activa
        if (
            self.estado == self.Estado.ACTIVA
            and self.bloque_id
            and hasattr(self.bloque, 'estado')
            and self.bloque.estado == Bloque.Estado.INACTIVO
        ):
            raise ValidationError(
                {'estado': 'No se puede tener un aula activa en un bloque inactivo.'}
            )