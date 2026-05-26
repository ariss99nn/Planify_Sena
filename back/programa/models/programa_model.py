from django.db import models


class Programa(models.Model):

    class Nivel(models.TextChoices):
        TECNICO     = 'TECNICO',     'Tecnico'
        TECNOLOGIA  = 'TECNOLOGIA',  'Tecnologia'
        CURSO_CORTO = 'CURSO_CORTO', 'Curso Corto'

    class Estado(models.TextChoices):
        ACTIVO     = 'ACTIVO',     'Activo'
        INACTIVO   = 'INACTIVO',   'Inactivo'
        EN_REVISION= 'EN_REVISION','En revision'

    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    nivel = models.CharField(
        max_length=20, choices=Nivel.choices,
        default=Nivel.TECNICO, db_index=True,
    )
    horas_lectivas  = models.PositiveIntegerField()
    horas_practicas = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20, choices=Estado.choices,
        default=Estado.ACTIVO, db_index=True,
    )
    trimestres_totales = models.PositiveIntegerField(
        default=6,
        help_text='Total de trimestres antes de etapa productiva.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Programa'
        verbose_name_plural = 'Programas'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_nivel_display()})"

    @property
    def total_horas(self):
        return self.horas_lectivas + self.horas_practicas