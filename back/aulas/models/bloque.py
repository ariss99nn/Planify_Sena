# aulas/models/bloque.py
from django.db import models
from users.validators import validate_imagen_5mb


class Bloque(models.Model):

    class Estado(models.TextChoices):           # CORRECCIÓN: Bloque necesita estado propio
        ACTIVO       = 'ACT',  'Activo'
        MANTENIMIENTO = 'MANT', 'Mantenimiento'
        INACTIVO     = 'INAC', 'Inactivo'

    nombre = models.CharField(max_length=50, unique=True)
    pisos  = models.PositiveIntegerField(       # CORRECCIÓN: renombrado de 'piso' a 'pisos' (semántica)
        help_text='Número de pisos del bloque.',
    )
    capacidad_maxima = models.PositiveIntegerField(
        help_text='Capacidad total de personas en el bloque.',
    )
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ACTIVO,
        db_index=True,
    )
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(
        upload_to='bloques/',
        null=True,
        blank=True,
        validators=[validate_imagen_5mb],
    )

    class Meta:
        verbose_name        = 'Bloque'
        verbose_name_plural = 'Bloques'
        ordering            = ['nombre']
        indexes = [
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return self.nombre

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.capacidad_maxima is not None and self.capacidad_maxima <= 0:
            raise ValidationError({'capacidad_maxima': 'La capacidad debe ser mayor a 0.'})
        if self.pisos is not None and self.pisos <= 0:
            raise ValidationError({'pisos': 'El número de pisos debe ser mayor a 0.'})