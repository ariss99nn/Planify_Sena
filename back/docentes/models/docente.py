# docentes/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from users.validators import validate_imagen


class Docente(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='docente',
        limit_choices_to={'rol': 'DOCENTE'},
    )
    especialidad = models.CharField(max_length=100)
    horas_max_semanales = models.PositiveIntegerField(
        help_text='Maximo de horas semanales asignables.',
    )
    estado = models.BooleanField(
        default=True, db_index=True,
        help_text='False = inactivo/retirado.',
    )
    imagen = models.ImageField(
        upload_to='docentes/', null=True, blank=True,
        validators=[validate_imagen],
    )

    class Meta:
        verbose_name        = 'Docente'
        verbose_name_plural = 'Docentes'
        ordering = ['user__apellido', 'user__nombre']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['especialidad']),
        ]

    def __str__(self):
        return f"{self.user.nombre_completo} -- {self.especialidad}"

    @property
    def nombre_completo(self):
        return self.user.nombre_completo

    @property
    def email(self):
        return self.user.email


