from django.db import models
from django.conf import settings
from programa.models.version_programa_model import VersionPrograma


class Ficha(models.Model):

    class Jornada(models.TextChoices):
        MANANA = 'MANANA', 'Mañana'
        TARDE = 'TARDE', 'Tarde'
        NOCHE = 'NOCHE', 'Noche'
        MIXTA = 'MIXTA', 'Mixta'

    class Etapa(models.TextChoices):
        LECTIVA = 'LECTIVA', 'Lectiva'
        PRODUCTIVA = 'PRODUCTIVA', 'Productiva'

    codigo_ficha = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )
    version = models.ForeignKey(
        VersionPrograma,
        on_delete=models.PROTECT,
        related_name='fichas',
    )
    jornada = models.CharField(
        max_length=10,
        choices=Jornada.choices,
        db_index=True,
    )
    numero_estudiantes_estimado = models.PositiveIntegerField(
        help_text='Cupo estimado al crear la ficha.',
    )
    etapa = models.CharField(
        max_length=15,
        choices=Etapa.choices,
        default=Etapa.LECTIVA,
        db_index=True,
    )
    horas_semanales_objetivo = models.PositiveIntegerField()
    trimestre = models.PositiveIntegerField(
        help_text='Trimestre de formación en curso.',
    )
    estado = models.BooleanField(default=True, db_index=True)
    cadena_formacion = models.BooleanField(
        default=False,
        help_text='Indica si la ficha está en cadena de formación.',
    )
    jefe_grupo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='fichas_jefe',
        limit_choices_to={'rol': 'DOCENTE'},
        null=True,
        blank=True,
    )
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'
        ordering = ['-fecha_inicio', 'codigo_ficha']
        indexes = [
            models.Index(fields=['estado', 'etapa']),
            models.Index(fields=['jornada']),
        ]

    def __str__(self):
        return f"Ficha {self.codigo_ficha} — {self.version.programa.nombre}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if (
            self.fecha_finalizacion
            and self.fecha_inicio
            and self.fecha_finalizacion < self.fecha_inicio
        ):
            raise ValidationError({
                'fecha_finalizacion': (
                    'La fecha de finalización no puede ser '
                    'anterior a la fecha de inicio.'
                )
            })
        
        trimestres_max = getattr(self.version.programa, 'trimestres_totales', None)
        if trimestres_max and self.trimestre > trimestres_max:
            raise ValidationError({
                'trimestre': f'El trimestre no puede superar {trimestres_max}.'
            })

    @property
    def programa(self):
        return self.version.programa

    @property
    def numero_estudiantes_real(self):
        return self.estudiantes.filter(activo=True).count()

    @property
    def trimestres_restantes(self):
        """Estimado de trimestres para llegar a etapa productiva."""
        if self.etapa == self.Etapa.PRODUCTIVA:
            return 0
        version_trimestres = getattr(
            self.version.programa, 'trimestres_totales', None
        )
        if version_trimestres:
            return max(0, version_trimestres - self.trimestre)
        return None